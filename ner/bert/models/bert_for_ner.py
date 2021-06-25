import torch
import torch.nn as nn

from .transformers import BertPreTrainedModel
from .transformers import BertModel

from .layers.crf import CRF
from .layers.normalization import LayerNorm

class BertCrfForNer(BertPreTrainedModel):
    def __init__(self, config):
        super(BertCrfForNer, self).__init__(config)
        self.bert = BertModel(config)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
        self.classifier = nn.Linear(config.hidden_size, config.num_labels)
        self.crf = CRF(num_tags=config.num_labels, batch_first=True)
        self.init_weights()

    def forward(self, input_ids, token_type_ids=None, attention_mask=None, labels=None, input_lens=None):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        sequence_output = outputs[0]
        sequence_output = self.dropout(sequence_output)
        logits = self.classifier(sequence_output)
        outputs = (logits,)
        if labels is not None:
            loss = self.crf(emissions=logits, tags=labels, mask=attention_mask)
            outputs = (-1 * loss,) + outputs
        return outputs  # (loss), scores

class BertLSTMCRF(BertPreTrainedModel):
    def __init__(self, config):
        super(BertLSTMCRF, self).__init__(config)
        self.bert = BertModel(config)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
        self.classifier = nn.Linear(config.hidden_size, config.num_labels)
        self.init_weights()

        self.num_layers = 2
        lstm_dropout = 0.35
        mdp_p = 0.5
        mdp_n = 5
        self.bilstm = nn.LSTM(input_size=config.hidden_size,
                              hidden_size=config.hidden_size // 2,
                              batch_first=True,
                              num_layers=self.num_layers,
                              dropout=lstm_dropout,
                              bidirectional=True)
        self.layer_norm = LayerNorm(config.hidden_size)
        self.dropouts = nn.ModuleList([
            nn.Dropout(mdp_p) for _ in range(mdp_n)
        ])
        self.crf = CRF(num_tags=config.num_labels, batch_first=True)

    def forward(self, input_ids, token_type_ids=None, attention_mask=None, labels=None, input_lens=None):
        self.bilstm.flatten_parameters()
        # self.rnn.flatten_parameters()

        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        sequence_output = outputs[0]
        sequence_output = self.dropout(sequence_output)
        sequence_output, hidden = self.bilstm(sequence_output)
        sequence_output = self.layer_norm(sequence_output)

        for i, dropout in enumerate(self.dropouts):
            if i == 0:
                logits = self.classifier(dropout(sequence_output))
            else:
                logits += self.classifier(dropout(sequence_output))
        # logits = self.classifier(sequence_output)
        logits = logits / len(self.dropouts)
        outputs = (logits,)
        if labels is not None:
            loss = self.crf(emissions=logits, tags=labels, mask=attention_mask)
            outputs = (-1 * loss,) + outputs
        return outputs  # (loss), scores
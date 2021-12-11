import torch
from typing import List, Tuple
from tokenizers import Tokenizer, Encoding


class DataBuilder:
    def __init__(self, tokenizer: Tokenizer, max_length: int):
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __call__(self, *args) -> torch.Tensor:
        raise NotImplementedError

    def encode(self, sents: List[str]) -> Tuple[torch.Tensor, torch.Tensor]:
        # we use enable padding here, rather than on creating the tokenizer,
        # to set maximum length on encoding
        self.tokenizer.enable_padding(pad_token=self.tokenizer.pad_token,  # noqa
                                      pad_id=self.tokenizer.pad_token_id,  # noqa
                                      length=self.max_length)
        # don't add special tokens, we will add them ourselves
        encodings: List[Encoding] = self.tokenizer.encode_batch(sents, add_special_tokens=False)
        input_ids = torch.LongTensor([encoding.ids for encoding in encodings])
        # 1's: non-pad tokens. 0's: padded tokens
        mask = torch.LongTensor([encoding.attention_mask for encoding in encodings])
        return input_ids, mask


class TrainInputsBuilder(DataBuilder):

    def __call__(self, srcs: List[str], tgts: List[str]) -> torch.Tensor:
        """
        :param srcs:
        :param tgts:
        :return: (N, 2, 2, L) - input_ids & attention_mask
        """
        # the source sentences, which are to be fed as the inputs to the encoder
        input_ids_src, attention_mask_src = self.encode([
            self.tokenizer.bos_token + " " + sent + " " + self.tokenizer.eos_token  # noqa
            for sent in srcs
        ])
        # the target sentences, which are to be fed as the inputs to the decoder
        input_ids_tgt, attention_mask_tgt = self.encode([
            # starts with bos, but does not end with eos (pad token is ignored anyways)
            self.tokenizer.bos_token + " " + sent  # noqa
            for sent in tgts
        ])
        inputs_src = torch.stack([input_ids_src, attention_mask_src], dim=1)
        inputs_tgt = torch.stack([input_ids_tgt, attention_mask_tgt], dim=1)
        inputs = torch.stack([inputs_src, inputs_tgt], dim=1)
        return inputs


class InferInputsBuilder(DataBuilder):
    def __call__(self, srcs: List[str]) -> torch.Tensor:
        """
        :param srcs:
        :return: (N, 2, L)
        """
        # the source sentences, which are to be fed as the inputs to the encoder
        input_ids_src, attention_mask_src = self.encode([
            self.tokenizer.bos_token + " " + sent + " " + self.tokenizer.eos_token  # noqa
            for sent in srcs
        ])
        input_ids_tgt, attention_mask_tgt = self.encode([
            # just start with bos_token.
            # why no eos token at the end?
            # A: because the label for eos token, i.e. pad token, is ignored in computing the loss anyways
            # also, this may lead to the model repeating characters
            # refer to: https://discuss.pytorch.org/t/transformer-mask-doesnt-do-anything/79765
            self.tokenizer.bos_token  # noqa
            for _ in srcs
        ])
        inputs_src = torch.stack([input_ids_src, attention_mask_src], dim=1)
        inputs_tgt = torch.stack([input_ids_tgt, attention_mask_tgt], dim=1)
        inputs = torch.stack([inputs_src, inputs_tgt], dim=1)
        return inputs


class LabelsBuilder(DataBuilder):

    def __call__(self, tgts: List[str]):
        """
        :param tgts:
        :return: (N, L)
        """
        # to be used as the labels
        input_ids, _ = self.encode([
            # does not start with bos, but ends with eos (right-shifted)
            sent + " " + self.tokenizer.eos_token  # noqa
            for sent in tgts
        ])
        return input_ids
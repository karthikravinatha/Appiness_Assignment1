# import json
# import os
# import pickle
#
# import torch
# # import gradio as gr
# import time
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
# from redis_helper import RedisCacheManager
#
# # from flores200_codes import flores_codes
#
#
# global model_dict
# global model
# global token
#
#
# def load_models():
#     # build model and tokenizer
#     model_name_dict = {'nllb-distilled-600M': 'facebook/nllb-200-distilled-600M',
#                        # 'nllb-1.3B': 'facebook/nllb-200-1.3B',
#                        # 'nllb-distilled-1.3B': 'facebook/nllb-200-distilled-1.3B',
#                        # 'nllb-3.3B': 'facebook/nllb-200-3.3B',
#                        }
#
#     model_dict = {}
#
#     for call_name, real_name in model_name_dict.items():
#         print('\tLoading model: %s' % call_name)
#         model = AutoModelForSeq2SeqLM.from_pretrained(real_name)
#         tokenizer = AutoTokenizer.from_pretrained(real_name)
#         model_dict[call_name + '_model'] = model
#         model_dict[call_name + '_tokenizer'] = tokenizer
#
#     return model_dict
#
#
# def translation(source='eng_Latn', target='kan_Knda', text="hello how are you"):
#     # if len(model_dict) == 2:
#     #     model_name = 'nllb-distilled-600M'
#
#     start_time = time.time()
#     # source = flores_codes[source]
#     # target = flores_codes[target]
#
#     # model = model_dict[model_name + '_model']
#     # tokenizer = model_dict[model_name + '_tokenizer']
#
#     translator = pipeline('translation', model=model, tokenizer=token, src_lang=source, tgt_lang=target)
#     output = translator(text, max_length=400)
#
#     end_time = time.time()
#
#     output = output[0]['translation_text']
#     result = {'inference_time': end_time - start_time,
#               'source': source,
#               'target': target,
#               'result': output}
#     return result
#
#
# # model_dict = load_models()
# # model_name = 'nllb-distilled-600M'
# # model = model_dict[model_name + '_model']
# # tokenizer = model_dict[model_name + '_tokenizer']
# # rob = RedisCacheManager()
# # rob.connect()
# # rob.put_obj_in_cache("nllb-600M-model", model_dict)
# # rob.get_object_cache("nllb-600M-model")
# #
# # with open("nllb_model.txt", "wb") as file:
# #     data = pickle.dumps(model)
# #     file.write(data)
#
# with open("nllb_model.txt", "rb") as fm:
#     fd = fm.read()
# model = pickle.loads(fd)
#
# with open("nllb_token.txt", "rb") as ft:
#     ft = ft.read()
# token = pickle.loads(fd)
# # model_dict = fd
# tr = translation()
# print(tr)
# print(tr)
# print(tr)






















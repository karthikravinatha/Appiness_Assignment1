# import os
# import time
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline, \
#     AutoModelForSequenceClassification
#
# from DemoProject.settings import BASE_DIR
#
# start = time.time()
# # tokenizer: AutoTokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
# # model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
# # #
# # #
# # translator = pipeline('translation', model=model, tokenizer=tokenizer, src_lang='eng_Latn', tgt_lang='deu_Latn',
# #                       max_length=500)
# # print(translator("hello how are you"))
# #
# # tokenizer = AutoModelForSequenceClassification.from_pretrained("facebook/nllb-200-distilled-600M")
# # model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
#
# # tokenizer.save_pretrained(BASE_DIR)
# # model.save_pretrained(BASE_DIR)
#
# # model_path = os.path.join(BASE_DIR, "trained_model")
# # model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
# # translator = pipeline('translation', model=model, tokenizer=tokenizer, src_lang='eng_Latn', tgt_lang='tel_Telu',
# #                       max_length=500)
# # print(translator("hello how are you"))
# #
# # en_fr_translator = pipeline("translation","translation_en_to_fr")
# # # translator = pipeline("translation", model=model_checkpoint)
# # en_fr_translator("How old are you?")
#
# # model_checkpoint = "Helsinki-NLP/opus-mt-en-fr"
# # model_checkpoint = "Helsinki-NLP/opus-mt-en-fr"
# # translator = pipeline("translation", model=model_checkpoint)
# # translator = pipeline('translation', model=translator.model, tokenizer=translator.tokenizer,
# #                       max_length=500)
# # translator("How are you?")
#
#
# # tokenizer: AutoTokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
# # model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
# model_checkpoint = "Helsinki-NLP/opus-mt-en-fr"
# translator = pipeline("translation", model=model_checkpoint)
# model_path = os.path.join(BASE_DIR, "trained_model")
# #
# #
# translator = pipeline('translation', model=translator.model, tokenizer=translator.tokenizer,
#                       # src_lang='eng_Latn', tgt_lang='kan_Knda',
#                       max_length=500)
# print(translator("hello how are you"))
# import pdb
#
# pdb.set_trace()
# print(type(translator))
# end = time.time()
# print(start - end)


import asyncio
from itertools import chain


#
# async def my_task():
#     print("Task started")
#     await asyncio.sleep(2)  # Simulate a delay of 2 seconds
#     print("Task completed")
#
# async def delayed_task():
#     # await asyncio.sleep(1)  # Simulate a delay of 1 second
#     await my_task()
#
# async def main():
#     print("Before delay")
#     asyncio.create_task(delayed_task())
#     print("After delay")
#
# asyncio.run(main())


# import asyncio
#
# def async_call_later(seconds, callback):
#     async def schedule():
#         await asyncio.sleep(seconds)
#
#         if asyncio.iscoroutinefunction(callback):
#             await callback()
#         else:
#             callback()
#
#     asyncio.ensure_future(schedule())
#
# async def do_something_async():
#     await asyncio.sleep(0.5)
#     print('Now! async')
#
# async def main():
#     print('Scheduling...')
#     loop = asyncio.get_event_loop()
#     async_call_later(3, do_something_async)
#     async_call_later(3, lambda: print('Now!'))
#
#     print('Waiting...')
#
#     await asyncio.sleep(4)
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

async def method1():
    # await asyncio.sleep(1)
    print("method1 is calling")


async def main():
    print("start ....")
    asyncio.create_task(method1())
    print("middle ....")
    print("end ...")


asyncio.run(main())


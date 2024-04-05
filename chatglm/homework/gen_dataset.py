import csv
import datetime
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# from langchain.prompts.chat import (
#     ChatPromptTemplate,
#     HumanMessagePromptTemplate,
#     SystemMessagePromptTemplate,
# )


class GenDataSet:
    system_message = None
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-1106",
        base_url="https://api.132006.xyz/v1",
        openai_api_key="sk-Bx6gwmNV6GUul9lE7bF358Fe33Da43Af8444543860F2D2Ce",
        temperature=1,
        max_tokens=4095,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # human_message = None
    def __init__(self, system_message):
        self.system_message = system_message
        self.__main()

    def __gen_data(self, raw_content):
        human_message = HumanMessage(content=raw_content)
        messages = [self.system_message, human_message]
        ai_message = self.chat(messages)
        return ai_message.content

    def __dataset_parser(self, ai_message_content):
        # 分割字符串来找到content和summary的位置
        content_start = ai_message_content.find('content:"') + len('content:"')
        content_end = ai_message_content.find('"\nsummary:')
        summary_start = ai_message_content.find('summary:"') + len('summary:"')
        summary_end = ai_message_content.rfind('"')

        # 提取并存储content和summary
        content = ai_message_content[content_start:content_end].strip()
        summary = ai_message_content[summary_start:summary_end].strip()

        return content, summary

    def __generate_question_summary_pairs(self, content, summary):
        question_templates = [
            "{}代表什么？",
            "周易中的{}含义是什么？",
            "请解释一下{}。",
            "{}在周易中是什么象征？",
            "周易{}的深层含义是什么？",
            "{}和教育启蒙有什么联系？",
            "周易的{}讲述了什么？",
            "{}是怎样的一个卦象？",
            "{}在周易中怎样表达教育的概念？",
            "{}的基本意义是什么？",
            "周易中{}的解释是什么？",
            "{}在周易中代表了哪些方面？",
            "{}涉及哪些哲学思想？",
            "周易中{}的象征意义是什么？",
            "{}的主要讲述内容是什么？",
            "周易{}的核心思想是什么？",
            "{}和启蒙教育之间有何联系？",
            "在周易中，{}象征着什么？",
            "请描述{}的含义。",
            "{}在周易哲学中扮演什么角色？",
        ]
        questions = [template.format(content) for template in question_templates]

        question_summary_pairs = [(question, summary) for question in questions]

        return question_summary_pairs

    def __main(self):
        if not os.path.exists("document/LLM-quickstart/chatglm/data"):
            os.makedirs("document/LLM-quickstart/chatglm/data")

        raw_content_data = []

        with open(
            "document/LLM-quickstart/chatglm/data/raw_data.txt", "r", encoding="utf-8"
        ) as file:
            content = file.read()
            data_samples = content.split("\n\n")
            for sample in data_samples:
                cleaned_sample = sample.strip()
                if cleaned_sample:
                    raw_content_data.append(cleaned_sample)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"document/LLM-quickstart/chatglm/data/zhouyi_dataset_{timestamp}.csv"

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["content", "summary"])
            for raw_content in raw_content_data:
                ai_message_content = self.__gen_data(raw_content)
                content, summary = self.__dataset_parser(ai_message_content)

                print("Content:", content)
                print("Summary:", summary)
                pairs = self.__generate_question_summary_pairs(content, summary)

                # 将 pairs 写入 csv 文件
                for pair in pairs:
                    writer.writerow(pair)


# 系统消息定义背景和任务
system_message = SystemMessage(
    content="""
        你是中国古典哲学大师，尤其擅长周易的哲学解读。

        接下来，你收到的都是关于周易卦象的解释，你需要整理润色，并生成用于大模型训练的内容和格式。

        示例输入：

        师卦，此卦是异卦相叠，下卦为坎，上卦为坤。“师”指军队。坎为水、为险；坤为地、为顺，喻寓兵于农。兵凶战危，用兵乃圣人不得已而为之，但它可以顺利无阻碍地解决矛盾，因为顺乎形势，师出有名，故能化凶为吉。占得此卦，对于军事上率师出征非常有利，必无灾祸。师卦是天马出群之卦，以寡伏众之象。
        师卦位于讼卦之后，《序卦》之中这样解释道：“讼必有众起，故受之以师。师者，众也。”争讼的人越来越多，以致形成了军队。

        期待结果：

        content:"师卦"
        summary:"在周易中，师卦是一个极具深意的卦象，它由两个异卦相叠组成：下卦坎（水）和上卦坤（地）。这一卦象代表“师”，即军队，寓意着兵力和农力的结合。在这里，坎卦象征着水和险难，而坤卦象征着地和顺从，暗示着通过将军事力量安置于民间，可以在必要时顺利调动。

        师卦的核心哲学是：虽然兵力代表着危险和战争，但其使用应当是圣人不得已而为之的最后手段。在正确的情况下，军事力量可以顺应形势，将危险转化为吉祥。因此，在军事策略上，此卦象征着出征将会顺利，无灾祸。

        师卦紧随讼卦（争讼卦），在《序卦》中解释为“讼必有众起，故受之以师”。这意味着争端激化至众多人群的参与，形成了类似军队的集体力量。"

        返回格式要求：
        content:"{卦名}"
        summary:"{内容}"
        """
)
# 测试
gen_data_result = GenDataSet(system_message=system_message)

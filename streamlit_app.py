import streamlit as st
import pandas as pd
import time
import random



class TreeNode(object):
    """
    feat 分类特征
    depth 节点深度
    data 节点数据
    node_id 节点编号
    father_id 父节点编号

    """
    def __init__(self, feat='无', value='无', data=None, depth=None, node_id=-1):
        self.feat = feat
        self.value = value
        self.depth = depth
        self.data = data
        self.children = []
        self.node_id = node_id
        
    def add_child(self, child):
        self.children.append(child)

def data_split(feat, data_df):
    unique_values = qna_dict[feat]['options']
    data_dict = {elem: pd.DataFrame for elem in unique_values}
    for key in data_dict.keys():
        data_dict[key] = data_df[:][data_df[feat] == key]
    return data_dict

# 数据

dataSet = [
    ["蜀国", "男", "智力中", "战斗力中", "外貌出众", '赵云'],
    ["魏国", "男", "智力中", "战斗力中", "外貌平凡", '夏侯渊'],
    ["吴国", "男", "智力中", "战斗力高", "外貌出众", '周瑜'],
    ["魏国", "男", "智力中", "战斗力高", "外貌平凡", '典韦'],
    ["蜀国", "男", "智力高", "战斗力中", "外貌出众", '诸葛亮'],
    ["吴国", "女", "智力中", "战斗力中", "外貌出众", '小乔'],
    ["蜀国", "女", "智力中", "战斗力高", "外貌出众", '糜夫人'],
    ["蜀国", "女", "智力中", "战斗力高", "外貌平凡", '黄月英'],
    ["吴国", "女", "智力中", "战斗力高", "外貌出众", '大乔'],
    ["魏国", "女", "智力高", "战斗力高", "外貌出众", '张春华']
]
labels = ['国家', '性别', '智力', '战斗力', '外貌', 'Name']

data_df = pd.DataFrame(dataSet, columns=labels)

###########
# 开始游戏 #
###########


st.title("🌲构建你的《三国策》决策树🌲")

# 设置分类特征对应的问题（optional）

if st.checkbox('请输入每个分类特征对应的问题：'):
    qna_dict = {
                "性别":{'label':"请问阁下是一个纯爷们么？", 'options':("男", "女")},
                "智力":{'label':"请问阁下是否喜欢琢磨智力游戏？", 'options':("智力高", "智力中")},
                "战斗力":{'label':"请问阁下是否越挫越勇如同打不死的小强吗？", 'options':("战斗力高", "战斗力中")},
                "国家":{'label':"请问阁下推崇“遥遥领先”、“中庸之道”还是“后来居上”？", 'options':("魏国", "吴国", "蜀国")},
                "外貌":{'label':"请问阁下是否天生丽质？", 'options':("外貌出众", "外貌平凡")},
    }

    with st.form("question_generation"):
        for feat in qna_dict.keys():
            qst = st.text_input(
                f'请输入关于特征【{feat}】分类时，你想询问的问题：', 
                '')
            if qst != '':
                qna_dict[feat]['label'] = qst
        # Every form must have a submit button.
        submitted = st.form_submit_button("提交")
        if submitted:
            st.write('所有特征分类时的问题构建✅')
            for feat in qna_dict.keys():
                qst = qna_dict[feat]['label']
                st.write(f'特征{feat}的分类问题为：{qst}')


    if st.checkbox('构建决策树第一层'):

        # 第零层

        feat_list = []
        # Example:
        # feat_list = [
        #     'Nation', 
        #     ['Root', 'Knock', 'Texture'],
        #     [['Texture', 'Umbilical'], ['Texture', None], ['Root', 'Knock']]
        # ]

        root = TreeNode(data=data_df,depth = 0)
        index = 0



        
        # 第一层

        with st.form("frist_lev_feat_sel"):
            option = st.selectbox(
            "请选择1个决策树第一层分类依据的特征：",
            ['国家', '性别', '智力', '战斗力', '外貌', "无"],
            index=5)
            feat_list.append(option)
            # Every form must have a submit button.
            submitted = st.form_submit_button("提交")
            if submitted:
                st.write('决策树第一层构建完成✅')
                # st.write('你选择了', option)
                # st.write("feat_list", feat_list)


        if st.checkbox('构建决策树第二层'):
            depth = 1
            feat = feat_list[depth-1]

            if feat == '无':
                child = TreeNode(depth=depth, node_id=index)
                root.add_child(child)
                index += 1
            else:
                data_dict = data_split(feat, root.data)
                for value, data in data_dict.items():
                    child = TreeNode(feat, value, data, depth, index)
                    root.add_child(child)
                    index += 1

            # len(root.children): first_num

        
        
            # 第二层

            with st.form("second_lev_feat_sel"):
                second_feat_list = []
                for i, node in enumerate(root.children):
                    option = st.selectbox(
                    f"{i+1}：请选择决策树第二层，在【{node.feat}】取值为['{node.value}']的数据下，继续分类依据的特征：", 
                        ['国家', '性别', '智力', '战斗力', '外貌', '无'],
                        index=5)
                    second_feat_list.append(option)
                feat_list.append(second_feat_list)
                # Every form must have a submit button.
                submitted = st.form_submit_button("提交")
                if submitted:
                    st.write('决策树第二层构建完成✅')
                    # st.write('你选择了', second_feat_list)
                    # st.write("feat_list", feat_list)
            
            if st.checkbox('确定构建决策树第三层'):
                depth = 2
                for i, node in enumerate(root.children):
                    feat = feat_list[depth-1][i]
                    if feat == '无':
                        child = TreeNode(depth=depth, node_id=index)
                        node.add_child(child)
                        index += 1
                        continue
                    data_dict = data_split(feat, node.data)
                    for value, data in data_dict.items():
                        child = TreeNode(feat, value, data, depth, index)
                        node.add_child(child)
                        index += 1

                # len(root.children[i].children): second_num in second_num_list

            
                
                # 第三层
                level_2 = root.children

                with st.form("third_lev_feat_sel"):
                    # last_feat_list = feat_list[depth-1]
                    third_feat_list = []
                    for i, node1 in enumerate(root.children):
                        last_ans_list = []
                        for node2 in node1.children:
                            last_feat = node2.feat
                            last_ans_list.append(node2.value)
                        options = st.multiselect(
                            f"{i+1}：请选择决策树第三层，在【{last_feat}】的取值分别为{last_ans_list}的数据下，继续分类依据的特征：",
                            ['国家', '性别', '智力', '战斗力', '外貌', '无']*len(last_ans_list),
                            default=['无']*len(last_ans_list))
                        third_feat_list.append(options)
                    feat_list.append(third_feat_list)
                    # Every form must have a submit button.
                    submitted = st.form_submit_button("提交")
                    if submitted:
                        st.write('决策树已构建完成✅')
                        time.sleep(1)
                        st.balloons()
                        # st.write('你选择了', third_feat_list)
                        # st.write("feat_list", feat_list)

                if st.checkbox('现在开始问答环节：'):
                    
                    depth = 3
                    for i, node1 in enumerate(root.children):
                        for j, node2 in enumerate(node1.children):
                            # print("i, j:", i, j)
                            feat = feat_list[depth-1][i][j]
                            if feat == '无':
                                child = TreeNode(depth=depth, node_id=index)
                                node2.add_child(child)
                                index += 1
                                continue
                            data_dict = data_split(feat, node2.data)
                            for value, data in data_dict.items():
                                child = TreeNode(feat, value, data, depth, index)
                                node2.add_child(child)
                                index += 1

                    # len(root.children[i].children[j].children): 2
                    
                    index = 1
                    while(root.children != []):
                        qst_feat = root.children[0].feat
                        if qst_feat == '无':
                            break
                        qst_temp = qna_dict[qst_feat]
                        qst_temp['label'] = f'{index}：' + qst_temp['label']
                        with st.form(f"{index}:question_and_answer"):
                            ans = st.radio(**qst_temp)
                            for child in root.children:
                                if child.value == ans:
                                    root = child
                                    break
                            index += 1
                            submitted = st.form_submit_button("提交")
                        if submitted:
                            st.write('回答完成✅')
                    name_list = root.data['Name'].to_list()
                    # st.write("name_list", name_list)

                    if st.checkbox('看看你是谁：'):
                        name_pic_dict = {
                                    '赵云': 'https://staticcdn.boyuai.com/user-assets/34/pMpxwarVGsmucgnQmsyyMJ/三国策-01.jpg!jpg',
                                    '夏侯渊': 'https://staticcdn.boyuai.com/user-assets/34/dEC7ZBZZ9HihKwW5oCkbRc/三国策-02.jpg!jpg',
                                    '周瑜': 'https://staticcdn.boyuai.com/user-assets/34/ZQvZzdwKBGptsAfyptVQs4/三国策-03.jpg!jpg',
                                    '典韦': 'https://staticcdn.boyuai.com/user-assets/34/8hfAYrabtH6MDMXzW9zokS/三国策-04.jpg!jpg',
                                    '诸葛亮': 'https://staticcdn.boyuai.com/user-assets/34/miz5hvZ8iNgx22YJZRRXLG/三国策-05.jpg!jpg',
                                    '小乔': 'https://staticcdn.boyuai.com/user-assets/34/2igBq7v2y6qB2PbtN1FfGZ/三国策-06.jpg!jpg',
                                    '糜夫人': 'https://staticcdn.boyuai.com/user-assets/34/ZM9jyLJQ9YtN7Jak82mX4t/三国策-07.jpg!jpg',
                                    '黄月英': 'https://staticcdn.boyuai.com/user-assets/34/SFU5TxfoVncuT3hsZD458N/三国策-08.jpg!jpg',
                                    '大乔': 'https://staticcdn.boyuai.com/user-assets/34/cEhwSgzg4vXyMGKQRWm3PG/三国策-09.jpg!jpg',
                                    '张春华': 'https://staticcdn.boyuai.com/user-assets/34/gkNZjcR6PFH9UtHUDH9hpC/三国策-10.jpg!jpg'
                        }

                        if name_list:
                            name = random.choice(name_list)
                            image = name_pic_dict[name]
                            st.image(image, width=300)
                            time.sleep(2)
                            st.balloons()
                        else:
                            st.write("很遗憾，三国策中找不到和你一样的人物诶😫")







# st.title("机器诗人的词藻")

# value = st.slider('请选择机器作诗的次数：', 1, 10, 1)

# word_dict = {}
# text = st.text_input("请输入智能写诗的主题（3个字以内哦）：")

# if text.strip() != "":
#     for i in range(value):
#         st.write(f"正在创作第{i+1}首以{text}为主题的诗词...")
#         data = {"text": text, "index": i}
#         while True:
#             poem_dict = client.request(url, data)
#             if 'poem' in poem_dict:
#                 break
#         poem = poem_dict['poem'][0]
#         time.sleep(0.5)
#         st.write(f'诗歌{i+1}：', poem['title'])
#         time.sleep(0.5)
#         st.write(poem['content'])
#     #     words_noun = [i.word for i in psg.cut(poem['content']) if i.flag.startswith("n")]
#         words_noun = [word for word in jieba.lcut(poem['content']) if word.strip() != ""]
#         for word in words_noun:
#             if word not in word_dict:
#                 word_dict[word] = 1
#             else:
#                 word_dict[word] += 1

# chart_data = pd.DataFrame(
#      sorted(word_dict.items(), key=lambda x : x[1], reverse=True)[:10],
#      columns=['词汇', '出现次数'])

# st.bar_chart(chart_data.set_index('词汇'))

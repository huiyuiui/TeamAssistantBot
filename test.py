# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# from imgurpython import ImgurClient
# import matplotlib as mpl
# # from matplotlib.font_manager import _rebuild
# mpl.rcParams['font.sans-serif']='Arial Unicode MS'
# mpl.rcParams['axes.unicode_minus']=False

# output = {'Main_task': '實作預測新聞是否受歡迎的模型', 'Subtasks': [{'Task': 'Task1', 'People': '1', 'Start_time': '10-22', 'End_time': '10-24'}, {'Task': '特徵工程', 'People': '1', 'Start_time': '10-23', 'End_time': '10-25'}, {'Task': '模型選擇與建立', 'People': '2', 'Start_time': '10-24', 'End_time': '10-26'}, {'Task': '模型評估與優化', 'People': '2', 'Start_time': '10-25', 'End_time': '10-27'}, {'Task': '撰寫報告與簡報', 'People': '1', 'Start_time': '10-26', 'End_time': '10-28'}]}

# # get schedule info (TBD)
# pre_df = pd.DataFrame(output)
# print(pre_df)

# # x-axis variable
# df = pd.json_normalize(pre_df['Subtasks'])[['Start_time', 'End_time', 'Task']]
# print(df)
# proj_start = df.Start_time.min()
# print(proj_start)

# df['start_num'] = (pd.to_datetime(df.Start_time, format='%m-%d') - pd.to_datetime(proj_start, format='%m-%d')).dt.days
# df['end_num'] = (pd.to_datetime(df.End_time, format='%m-%d') - pd.to_datetime(proj_start, format='%m-%d')).dt.days
# df['days_start_to_end'] = df.end_num - df.start_num


# # drawing
# fig, ax = plt.subplots(1, figsize=(16,5))
# ax.barh(df.Task, df.days_start_to_end, left=df.start_num)

# # Ticks
# xticks = np.arange(0, df. end_num.max()+1, 2)
# xticks_labels = pd.date_range(pd.to_datetime(proj_start, format='%m-%d'), end=pd.to_datetime(df.End_time, format='%m-%d').max()).strftime("%m/%d")
# xticks_minor = np.arange(0, df.end_num.max()+1, 1)
# ax.set_xticks(xticks)
# ax.set_xticks(xticks_minor, minor=True)
# ax.set_xticklabels(xticks_labels[::2])
# plt.show()

# plt.savefig('task_chart.png')
# client_id = '7ece996e29fd7dc'
# client_secret = '76157f82924e2ab9583e8d018cd6d01a5b767e75'
# client = ImgurClient(client_id, client_secret)

# image_path = 'task_chart.png'
# uploaded_image = client.upload_from_path(image_path, anon=True)

# image_url = uploaded_image['link']
# print(image_url)
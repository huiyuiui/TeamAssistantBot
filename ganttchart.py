# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# from matplotlib.patches import Patch
# from imgurpython import ImgurClient

# test = {
#     "Task": ["Task1", "Task2", "Task3", "Task4"],
#     "Start": ["2023-03-17", "2023-03-19", "2023-03-20", "2023-03-22"],
#     "End": ["2023-03-20", "2023-03-23", "2023-03-21", "2023-03-25"]
# }

# # get schedule info (TBD)
# df = pd.DataFrame(test)
# # append row's name (TBD)
#     # Start
#     # End
#     # Task

# # x-axis variable
# proj_start = df.Start.min()

# df['start_num'] = (pd.to_datetime(df.Start) - pd.to_datetime(proj_start)).dt.days
# df['end_num'] = (pd.to_datetime(df.End) - pd.to_datetime(proj_start)).dt.days
# df['days_start_to_end'] = df.end_num - df.start_num

# # drawing
# fig, ax = plt.subplots(1, figsize=(16,5))
# ax.barh(df.Task, df.days_start_to_end, left=df.start_num)

# # Ticks
# xticks = np.arange(0, df. end_num.max()+1, 2)
# xticks_labels = pd.date_range(proj_start, end=df.End.max()).strftime("%m/%d")
# xticks_minor = np.arange(0, df.end_num.max()+1, 1)
# ax.set_xticks(xticks)
# ax.set_xticks(xticks_minor, minor=True)
# ax.set_xticklabels(xticks_labels[::2])

# plt.savefig('task_chart.png')
# client_id = '7ece996e29fd7dc'
# client_secret = '76157f82924e2ab9583e8d018cd6d01a5b767e75'
# client = ImgurClient(client_id, client_secret)

# image_path = 'task_chart.png'
# uploaded_image = client.upload_from_path(image_path, anon=True)

# image_url = uploaded_image['link']
# plt.show()

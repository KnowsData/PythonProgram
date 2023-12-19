import warnings
warnings.simplefilter('ignore', FutureWarning)

import os
import glob
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import japanize_matplotlib
import re
import plotly.express as px
from IPython.display import display
from IPython.display import HTML




desktop_path = os.path.expanduser('~/Desktop')

# 変数を使ってフォルダ名を指定
print("\n")
print("【Individual Feedback】")
folder_name = input("Enter the folder name (This week) → ")

# CSVファイルのディレクトリパス
directory = fr"{desktop_path}/Knows/Training/{folder_name}"
    
# ディレクトリ内のすべてのCSVファイルのパスを取得
csv_files = glob.glob(os.path.join(directory, "*.csv"))

# 取得したファイルのリストを表示
for csv_file in csv_files:
    print(csv_file)
print("\n")
    
# データを保持するための辞書
data = {}

# CSVファイルの読み込み
for file_path in csv_files:
    file_name = os.path.basename(file_path)
    df = pd.read_csv(file_path)
    data[file_name] = df


# サブプロットを作成
fig = make_subplots(rows=3, cols=2, subplot_titles=("「Distance」", "「Sprint」", "「Accel All」", "「Decel All」", "「SPD MAX」"))

# 各データセットに好きな色を指定
colors = ['#636EFA', '#AB63FA', '#FF6692', '#EF553B', '#FFA15A', '#FECB52', '#B6E880', '#00CC96', '#19D3F3']


# すべてのデータを表示するためのボタンを作成
button_all = dict(
    label='All',
    method='update',
    args=[{'visible': [True] * len(csv_files)}, {'title': '【Feedback on Individual Player】　All'}],
)
buttons = [button_all]

def format_date(file_name):
    date_str = file_name.split('_')[1]  # '_'で分割し、日付部分を取得
    date_obj = datetime.strptime(date_str, "%Y%m%d")  # 文字列を日付オブジェクトに変換
    formatted_date = date_obj.strftime("%Y/%m/%d")  # 指定した形式に整形
    return formatted_date

# 各CSVファイルに対応するボタンを作成
for i, file_path in enumerate(csv_files):
    file_name = os.path.basename(file_path)
    visible = [False] * len(csv_files)
    visible[i] = True

    formatted_date = format_date(file_name)  # 日付を指定した形式に整形
    full_title = "&#8203;【Feedback on Individual Player】 &#8203; " + formatted_date  # 文字列を連結してタイトルを作成
    
    button = dict(
        label=formatted_date,  # 整形した日付をラベルとして設定
        method='update',
        args=[{'visible': visible}, {'title': full_title}],  # 整形した日付をタイトルとして設定
    )
    buttons.append(button)

# ボタンを追加
fig.update_layout(
    updatemenus=[
        dict(
            buttons=buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=1.0,
            xanchor="left",
            y=1.15,
            yanchor="top",
            active=0  # 初期状態で表示するボタン（All）
        ),
    ]
)


# 走行距離のグラフを追加
for i, (file, df) in enumerate(data.items()):
    date_str = file.split("_")[1]  # ファイル名から日付文字列を取得
    date_obj = datetime.strptime(date_str, "%Y%m%d")  # 8桁の数字をdatetimeオブジェクトに変換
    formatted_date = date_obj.strftime("%Y/%m/%d")  # 指定した形式に整形
    # Position列でデータフレームをソートしてからグラフを作成する
    df_sorted = df.sort_values('Position', key=lambda x: x.map({'FW': 0, 'MF': 1, 'DF': 2}))
    fig.add_trace(go.Bar(
        x=df_sorted['Name'],
        y=df_sorted['Distance'].round(0),
        name=f"「Distance」: {formatted_date}",
        marker_color=colors[i % len(colors)]
    ), row=1, col=1)

# スプリント回数のグラフを追加
for i, (file, df) in enumerate(data.items()):
    date_str = file.split("_")[1]  # ファイル名から日付文字列を取得
    date_obj = datetime.strptime(date_str, "%Y%m%d")  # 8桁の数字をdatetimeオブジェクトに変換
    formatted_date = date_obj.strftime("%Y/%m/%d")  # 指定した形式に整形
    # Position列でデータフレームをソートしてからグラフを作成する
    df_sorted = df.sort_values('Position', key=lambda x: x.map({'FW': 0, 'MF': 1, 'DF': 2}))
    
    fig.add_trace(go.Bar(
        x=df_sorted['Name'],
        y=df_sorted['Sprint'].round(0),
        name=f"「Sprint」: {formatted_date}",
        marker_color=colors[i % len(colors)]
    ), row=1, col=2)
    
# 加速数のグラフを追加
for i, (file, df) in enumerate(data.items()):
    date_str = file.split("_")[1]  # ファイル名から日付文字列を取得
    date_obj = datetime.strptime(date_str, "%Y%m%d")  # 8桁の数字をdatetimeオブジェクトに変換
    formatted_date = date_obj.strftime("%Y/%m/%d")  # 指定した形式に整形
    # Position列でデータフレームをソートしてからグラフを作成する
    df_sorted = df.sort_values('Position', key=lambda x: x.map({'FW': 0, 'MF': 1, 'DF': 2}))
    
    fig.add_trace(go.Bar(
        x=df_sorted['Name'],
        y=df_sorted['Accel All'].round(0),
        name=f"「Accel All」: {formatted_date}",
        marker_color=colors[i % len(colors)]
    ), row=2, col=1)
    
# 減速数のグラフを追加
for i, (file, df) in enumerate(data.items()):
    date_str = file.split("_")[1]  # ファイル名から日付文字列を取得
    date_obj = datetime.strptime(date_str, "%Y%m%d")  # 8桁の数字をdatetimeオブジェクトに変換
    formatted_date = date_obj.strftime("%Y/%m/%d")  # 指定した形式に整形
    # Position列でデータフレームをソートしてからグラフを作成する
    df_sorted = df.sort_values('Position', key=lambda x: x.map({'FW': 0, 'MF': 1, 'DF': 2}))
    
    fig.add_trace(go.Bar(
        x=df_sorted['Name'],
        y=df_sorted['Decel All'].round(0),
        name=f"「Decel All」: {formatted_date}",
        marker_color=colors[i % len(colors)]
    ), row=2, col=2)
    
# 最高速度のグラフを追加
for i, (file, df) in enumerate(data.items()):
    date_str = file.split("_")[1]  # ファイル名から日付文字列を取得
    date_obj = datetime.strptime(date_str, "%Y%m%d")  # 8桁の数字をdatetimeオブジェクトに変換
    formatted_date = date_obj.strftime("%Y/%m/%d")  # 指定した形式に整形
    # Position列でデータフレームをソートしてからグラフを作成する
    df_sorted = df.sort_values('Position', key=lambda x: x.map({'FW': 0, 'MF': 1, 'DF': 2}))
    
    fig.add_trace(go.Bar(
        x=df_sorted['Name'],
        y=df_sorted['SPD MX'].round(0),
        name=f"「SPD MAX」: {formatted_date}",
        marker_color=colors[i % len(colors)]
    ), row=3, col=1)
    
# 全体の平均値を計算
mean_distance = pd.concat([df['Distance'] for df in data.values()]).mean()
mean_sprint = pd.concat([df['Sprint'] for df in data.values()]).mean()
mean_accel = pd.concat([df['Accel All'] for df in data.values()]).mean()
mean_decel = pd.concat([df['Decel All'] for df in data.values()]).mean()
mean_maxspd = pd.concat([df['SPD MX'] for df in data.values()]).mean()

# 平均値の水平線を追加
fig.add_hline(y=mean_distance, line_dash="dash", line_color="red", line_width=2, opacity=0.7, row=1, col=1)
fig.add_hline(y=mean_sprint, line_dash="dash", line_color="red", line_width=2, opacity=0.7, row=1, col=2)
fig.add_hline(y=mean_accel, line_dash="dash", line_color="red", line_width=2, opacity=0.7, row=2, col=1)
fig.add_hline(y=mean_decel, line_dash="dash", line_color="red", line_width=2, opacity=0.7, row=2, col=2)
fig.add_hline(y=mean_maxspd, line_dash="dash", line_color="red", line_width=2, opacity=0.7, row=3, col=1)

# グラフのレイアウト設定
fig.update_layout(
    title={
        'text': "【Feedback on Individual Player】",
        'font': {'size': 20}  # タイトルの文字の大きさを指定します
    },
    showlegend=True
)

# 縦軸名と横軸名を設定
fig.update_yaxes(title_text="(m)", row=1, col=1)
fig.update_yaxes(title_text="(Times)", row=1, col=2)
fig.update_yaxes(title_text="(Times)", row=2, col=1)
fig.update_yaxes(title_text="(Times)", row=2, col=2)
fig.update_yaxes(title_text="(Times)", row=3, col=1)

# HTMLファイルに保存
fig.write_html(f"{desktop_path}/Knows/Training/{folder_name}/Data2.html", auto_open=False)









# ユーザーからの入力を受け取り、4つのファイル名を指定
selected_files = []
print("【Team Feedback】")
time_periods = ["(This week)", "(1 week ago)", "(2 weeks ago)", "(3 weeks ago)"]

for i, time_period in enumerate(time_periods):
    file_name = input(f"Enter the folder name {time_period} → ")
    selected_files.append(file_name)

# ファイルからデータフレームを作成する関数
def create_dataframe_from_files(file_list):
    week_dataframes = {}
    
    for file_name in file_list:
        week_data = {}
        
        # CSVファイルのリストを取得
        csv_files = [f for f in os.listdir(f"{desktop_path}/Knows/Training/{file_name}") if f.endswith(".csv")]
        
        for csv_file in csv_files:
            # 正規表現を使用して日付部分を抜き出す
            match = re.search(r'(\d{8})', csv_file)
            if match:
                date_part = match.group(1)
                formatted_date = f"{date_part[:4]}/{date_part[4:6]}/{date_part[6:]}"
                
                file_path = os.path.join(f"{desktop_path}/Knows/Training/{file_name}", csv_file)
                df = pd.read_csv(file_path)
                
                # "Distance"、"Sprint"、"Accel All"、"Decel ALl"のみの平均値を計算し、四捨五入
                selected_columns = ["Distance", "Sprint", "Accel All", "Decel All"]
                mean_values = df[selected_columns].mean().round().astype(int)
                
                # ファイル名を日付に変更して列名としてデータを格納
                week_data[formatted_date] = mean_values
        
        # データフレームを作成
        week_df = pd.DataFrame(week_data)
        
        # Week1、Week2、Week3、Week4に対応するデータフレームを格納
        week_dataframes[f"Week{file_list.index(file_name) + 1}"] = week_df
    
    return week_dataframes

# データフレームを作成
weekly_dataframes = create_dataframe_from_files(selected_files)

# Week1、Week2、Week3、Week4のデータフレームにアクセス
week1_df = weekly_dataframes["Week1"]
week2_df = weekly_dataframes["Week2"]
week3_df = weekly_dataframes["Week3"]
week4_df = weekly_dataframes["Week4"]







# 1番目と2番目に選択されたフォルダ内のCSVファイルをそれぞれ処理するための関数
def process_selected_folders(folder1, folder2):
    # 1番目のフォルダからグラフを作成
    selected_folder_1 = os.path.join(f"{desktop_path}/Knows/Training", folder1)
    files_folder_1 = [f[:-4] for f in os.listdir(selected_folder_1) if f.endswith(".csv")]

    # 2番目のフォルダからグラフを作成
    selected_folder_2 = os.path.join(f"{desktop_path}/Knows/Training", folder2)
    files_folder_2 = [f[:-4] for f in os.listdir(selected_folder_2) if f.endswith(".csv")]

    # 3つのサブプロットを持つ図を作成
    fig = make_subplots(rows=2, cols=2, subplot_titles=("「Distance」", "「14~21km/h」", "「21~km/h」"))

    
    # 1番目のフォルダから選択されたCSV以外のデータを取得し、グラフに追加
    selected_file_1 = input(f"Choose a Game CSV file from {folder1} folder (Type 'No' to skip) → ")
    selected_files_1 = [file for file in files_folder_1 if file != selected_file_1]
    
    colors = ['#636EFA', '#AB63FA', '#FF6692', '#EF553B', '#FFA15A', '#FECB52', '#B6E880', '#00CC96', '#19D3F3']  # 使用したい色のリストを定義
    
    # グラフに積み重ねた最終的な値を表示するためのリストを作成
    final_values_distance = {}
    final_values_spd_z34 = {}
    final_values_spd_z56 = {}
    
    for idx, file in enumerate(selected_files_1):
        # 日付部分を正規表現で抜き出して整形
        match = re.search(r'_(\d{4})(\d{2})(\d{2})_', file)
        if match:
            year, month, day = match.groups()
            formatted_date = f"{year}/{month}/{day}"

            df = pd.read_csv(os.path.join(selected_folder_1, file + ".csv"))
            
            # グラフに要素を追加（積み重ねグラフに変更）
            # Distanceグラフ
            distance_data = df['Distance']
            fig.add_trace(go.Bar(x=df['Name'], y=distance_data, name=formatted_date, legendgroup=f"group{idx+1}", marker_color=colors[idx % len(colors)]), row=1, col=1)
            final_values_distance = {name: value + final_values_distance.get(name, 0) for name, value in zip(df['Name'], distance_data)}

            # SPD_D_Z3 + SPD_D_Z4グラフ
            spd_z34_data = df['SPD_D_Z3'] + df['SPD_D_Z4']
            fig.add_trace(go.Bar(x=df['Name'], y=spd_z34_data, name=formatted_date, legendgroup=f"group{idx+1}", marker_color=colors[idx % len(colors)]), row=1, col=2)
            final_values_spd_z34 = {name: value + final_values_spd_z34.get(name, 0) for name, value in zip(df['Name'], spd_z34_data)}

            # SPD_D_Z5 + SPD_D_Z6グラフ
            spd_z56_data = df['SPD_D_Z5'] + df['SPD_D_Z6']
            fig.add_trace(go.Bar(x=df['Name'], y=spd_z56_data, name=formatted_date, legendgroup=f"group{idx+1}", marker_color=colors[idx % len(colors)]), row=2, col=1)
            final_values_spd_z56 = {name: value + final_values_spd_z56.get(name, 0) for name, value in zip(df['Name'], spd_z56_data)}


            
    # 積み重ねグラフの上に最終的な値を表示
    for name, value in final_values_distance.items():
        if not pd.isnull(value):  # NaN（非数）値をチェックして除外
            rounded_value = int(value * 100) / 100
            final_value = f"{rounded_value / 1000:.1f}k" if rounded_value > 0 else "0"
            fig.add_trace(go.Scatter(x=[name], y=[value], mode='text', text=[final_value], textposition='top center', showlegend=False, marker=dict(color='rgba(0,0,0,0)')), row=1, col=1)

    for name, value in final_values_spd_z34.items():
        if not pd.isnull(value):  # NaN（非数）値をチェックして除外
            rounded_value = int(value * 100) / 100
            final_value = f"{rounded_value / 1000:.1f}k" if rounded_value > 0 else "0"
            fig.add_trace(go.Scatter(x=[name], y=[value], mode='text', text=[final_value], textposition='top center', showlegend=False, marker=dict(color='rgba(0,0,0,0)')), row=1, col=2)

    for name, value in final_values_spd_z56.items():
        if not pd.isnull(value):  # NaN（非数）値をチェックして除外
            rounded_value = int(value * 100) / 100
            final_value = f"{rounded_value / 1000:.1f}k" if rounded_value > 0 else "0"
            fig.add_trace(go.Scatter(x=[name], y=[value], mode='text', text=[final_value], textposition='top center', showlegend=False, marker=dict(color='rgba(0,0,0,0)')), row=2, col=1)



            
    # 2番目のフォルダから選択されたCSVを取得し、グラフに追加
    selected_file_2 = input(f"Choose a Game CSV file from {folder2} folder (Type 'No' to skip) → ")
    if selected_file_2.lower() != 'no' and selected_file_2 in files_folder_2:
        # 日付部分を正規表現で抜き出して整形
        match = re.search(r'_(\d{4})(\d{2})(\d{2})_', selected_file_2)
        if match:
            year, month, day = match.groups()
            formatted_date = f"{year}/{month}/{day}"
            
            df = pd.read_csv(os.path.join(selected_folder_2, selected_file_2 + ".csv"))
            # グラフに要素を追加
            # Distanceグラフ
            fig.add_trace(go.Scatter(x=df['Name'], y=df['Distance'] * 2.5, mode='markers', name=formatted_date, marker_color='black'), row=1, col=1)
            # SPD_D_Z3 + SPD_D_Z4グラフ
            fig.add_trace(go.Scatter(x=df['Name'], y=(df['SPD_D_Z3'] + df['SPD_D_Z4']) * 2.5, mode='markers', name=formatted_date, marker_color='black'), row=1, col=2)
            # SPD_D_Z5 + SPD_D_Z6グラフ
            fig.add_trace(go.Scatter(x=df['Name'], y=(df['SPD_D_Z5'] + df['SPD_D_Z6']) * 2.5, mode='markers', name=formatted_date, marker_color='black'), row=2, col=1)
                
            # グラフの上に数値を表示
            for name, value in zip(df['Name'], df['Distance'] * 2.5):
                if not pd.isnull(value):  # NaN（非数）値をチェックして除外
                    rounded_value = int(value * 100) / 100
                    final_value = f"{rounded_value / 1000:.1f}k" if rounded_value > 0 else "0"
                    fig.add_trace(go.Scatter(x=[name], y=[value], mode='text', text=[final_value], textposition='top center', showlegend=False, marker=dict(color='rgba(0,0,0,0)')), row=1, col=1)

            for name, value in zip(df['Name'], (df['SPD_D_Z3'] + df['SPD_D_Z4']) * 2.5):
                if not pd.isnull(value):  # NaN（非数）値をチェックして除外
                    rounded_value = int(value * 100) / 100
                    final_value = f"{rounded_value / 1000:.1f}k" if rounded_value > 0 else "0"
                    fig.add_trace(go.Scatter(x=[name], y=[value], mode='text', text=[final_value], textposition='top center', showlegend=False, marker=dict(color='rgba(0,0,0,0)')), row=1, col=2)

            for name, value in zip(df['Name'], (df['SPD_D_Z5'] + df['SPD_D_Z6']) * 2.5):
                if not pd.isnull(value):  # NaN（非数）値をチェックして除外
                    rounded_value = int(value * 100) / 100
                    final_value = f"{rounded_value / 1000:.1f}k" if rounded_value > 0 else "0"
                    fig.add_trace(go.Scatter(x=[name], y=[value], mode='text', text=[final_value], textposition='top center', showlegend=False, marker=dict(color='rgba(0,0,0,0)')), row=2, col=1)
    
  
       
    # グラフのレイアウトを設定
    fig.update_layout(
        title_text="【Compared with the Weekly Goal】",
        title_font_size=20,  # タイトルの文字の大きさを20に設定
        showlegend=True,
        barmode='stack'
    )

    # 縦軸名と横軸名を設定
    fig.update_yaxes(title_text="(m)", row=1, col=1)
    fig.update_yaxes(title_text="(m)", row=1, col=2)
    fig.update_yaxes(title_text="(m)", row=2, col=1)

    # HTMLファイルとして保存
    html_file_path = f"{desktop_path}/Knows/Training/{folder1}/Data3.html"
    fig.write_html(html_file_path)
    

    
# create_dataframe_from_files関数を実行してデータフレームを取得
weekly_dataframes = create_dataframe_from_files(selected_files)

# 1番目と2番目に選択されたフォルダ内のCSVファイルを処理
process_selected_folders(selected_files[0], selected_files[1])








# 既存のデータフレームから必要な値を抽出
week1_distance = week1_df.loc['Distance'].values
week2_distance = week2_df.loc['Distance'].values
week3_distance = week3_df.loc['Distance'].values
week4_distance = week4_df.loc['Distance'].values

# 新しいデータフレーム "Distance Table" を作成
distance_table = pd.DataFrame(columns=week1_df.columns)

# (1) DayAvg
distance_table.loc['Daily Avg'] = week1_distance

# (2) WeekAvg
week_avg = week1_distance.mean()
distance_table.loc['Weekly Avg'] = [week_avg] * len(week1_df.columns)

# (3) C Avg
c_avg = (week2_distance.mean() + week3_distance.mean() + week4_distance.mean()) / 3
distance_table.loc['C Avg'] = [c_avg] * len(week1_df.columns)

# (4) Day (%)
day_avg_row = distance_table.loc['Daily Avg']
c_avg_row = distance_table.loc['C Avg']
day_percent_row = (day_avg_row / c_avg_row * 100).astype(int).astype(str) + "%"
distance_table.loc['Daily (%)'] = day_percent_row

# (5) ThisWeek (%)
week_avg_row = distance_table.loc['Weekly Avg']
this_week_percent_row = (week_avg_row / c_avg_row * 100).astype(int).astype(str) + "%"
distance_table.loc['Weekly (%)'] = this_week_percent_row

# データフレーム内の指定した行名の値を整数に変換
# 例: Distance Tableの Day Avg, Week Avg, C Avg 行を整数に変換
distance_table.loc['Daily Avg'] = distance_table.loc['Daily Avg'].astype(int)
distance_table.loc['Weekly Avg'] = distance_table.loc['Weekly Avg'].astype(int)
distance_table.loc['C Avg'] = distance_table.loc['C Avg'].astype(int)





# 既存のデータフレームから必要な値を抽出
week1_sprint = week1_df.loc['Sprint'].values
week2_sprint = week2_df.loc['Sprint'].values
week3_sprint = week3_df.loc['Sprint'].values
week4_sprint = week4_df.loc['Sprint'].values

# 新しいデータフレーム "Distance Table" を作成
sprint_table = pd.DataFrame(columns=week1_df.columns)

# (1) DayAvg
sprint_table.loc['Daily Avg'] = week1_sprint

# (2) WeekAvg
week_avg = week1_sprint.mean()
sprint_table.loc['Weekly Avg'] = [week_avg] * len(week1_df.columns)

# (3) C Avg
c_avg = (week2_sprint.mean() + week3_sprint.mean() + week4_sprint.mean()) / 3
sprint_table.loc['C Avg'] = [c_avg] * len(week1_df.columns)

# (4) Day (%)
day_avg_row = sprint_table.loc['Daily Avg']
c_avg_row = sprint_table.loc['C Avg']
day_percent_row = (day_avg_row / c_avg_row * 100).astype(int).astype(str) + "%"
sprint_table.loc['Daily (%)'] = day_percent_row

# (5) ThisWeek (%)
week_avg_row = sprint_table.loc['Weekly Avg']
this_week_percent_row = (week_avg_row / c_avg_row * 100).astype(int).astype(str) + "%"
sprint_table.loc['Weekly (%)'] = this_week_percent_row

# データフレーム内の指定した行名の値を整数に変換
# 例: Distance Tableの Day Avg, Week Avg, C Avg 行を整数に変換
sprint_table.loc['Daily Avg'] = sprint_table.loc['Daily Avg'].astype(int)
sprint_table.loc['Weekly Avg'] = sprint_table.loc['Weekly Avg'].astype(int)
sprint_table.loc['C Avg'] = sprint_table.loc['C Avg'].astype(int)





# 既存のデータフレームから必要な値を抽出
week1_accel_all = week1_df.loc['Accel All'].values
week2_accel_all = week2_df.loc['Accel All'].values
week3_accel_all = week3_df.loc['Accel All'].values
week4_accel_all = week4_df.loc['Accel All'].values

# 新しいデータフレーム "Distance Table" を作成
accel_all_table = pd.DataFrame(columns=week1_df.columns)

# (1) DayAvg
accel_all_table.loc['Daily Avg'] = week1_accel_all

# (2) WeekAvg
week_avg = week1_accel_all.mean()
accel_all_table.loc['Weekly Avg'] = [week_avg] * len(week1_df.columns)

# (3) C Avg
c_avg = (week2_accel_all.mean() + week3_accel_all.mean() + week4_accel_all.mean()) / 3
accel_all_table.loc['C Avg'] = [c_avg] * len(week1_df.columns)

# (4) Day (%)
day_avg_row = accel_all_table.loc['Daily Avg']
c_avg_row = accel_all_table.loc['C Avg']
day_percent_row = (day_avg_row / c_avg_row * 100).astype(int).astype(str) + "%"
accel_all_table.loc['Daily (%)'] = day_percent_row

# (5) ThisWeek (%)
week_avg_row = accel_all_table.loc['Weekly Avg']
this_week_percent_row = (week_avg_row / c_avg_row * 100).astype(int).astype(str) + "%"
accel_all_table.loc['Weekly (%)'] = this_week_percent_row

# データフレーム内の指定した行名の値を整数に変換
# 例: Distance Tableの Day Avg, Week Avg, C Avg 行を整数に変換
accel_all_table.loc['Daily Avg'] = accel_all_table.loc['Daily Avg'].astype(int)
accel_all_table.loc['Weekly Avg'] = accel_all_table.loc['Weekly Avg'].astype(int)
accel_all_table.loc['C Avg'] = accel_all_table.loc['C Avg'].astype(int)





# 既存のデータフレームから必要な値を抽出
week1_decel_all = week1_df.loc['Decel All'].values
week2_decel_all = week2_df.loc['Decel All'].values
week3_decel_all = week3_df.loc['Decel All'].values
week4_decel_all = week4_df.loc['Decel All'].values

# 新しいデータフレーム "Distance Table" を作成
decel_all_table = pd.DataFrame(columns=week1_df.columns)

# (1) DayAvg
decel_all_table.loc['Daily Avg'] = week1_decel_all

# (2) WeekAvg
week_avg = week1_decel_all.mean()
decel_all_table.loc['Weekly Avg'] = [week_avg] * len(week1_df.columns)

# (3) C Avg
c_avg = (week2_decel_all.mean() + week3_decel_all.mean() + week4_decel_all.mean()) / 3
decel_all_table.loc['C Avg'] = [c_avg] * len(week1_df.columns)

# (4) Day (%)
day_avg_row = decel_all_table.loc['Daily Avg']
c_avg_row = decel_all_table.loc['C Avg']
day_percent_row = (day_avg_row / c_avg_row * 100).astype(int).astype(str) + "%"
decel_all_table.loc['Daily (%)'] = day_percent_row

# (5) ThisWeek (%)
week_avg_row = decel_all_table.loc['Weekly Avg']
this_week_percent_row = (week_avg_row / c_avg_row * 100).astype(int).astype(str) + "%"
decel_all_table.loc['Weekly (%)'] = this_week_percent_row

# データフレーム内の指定した行名の値を整数に変換
# 例: Distance Tableの Day Avg, Week Avg, C Avg 行を整数に変換
decel_all_table.loc['Daily Avg'] = decel_all_table.loc['Daily Avg'].astype(int)
decel_all_table.loc['Weekly Avg'] = decel_all_table.loc['Weekly Avg'].astype(int)
decel_all_table.loc['C Avg'] = decel_all_table.loc['C Avg'].astype(int)










# fig_distanceを作成
# データフレームから必要なデータを取得
distance_x = distance_table.columns
distance_y1 = distance_table.loc['Daily Avg']
distance_y2 = distance_table.loc['Daily (%)'].str.rstrip('%').astype(float)  # 「Day (%)」を数値に変換
distance_y3 = distance_table.loc['Weekly (%)'].str.rstrip('%').astype(float)  # 「Week (%)」を数値に変換

# 2軸グラフの作成
fig_distance = go.Figure()

# 棒グラフを追加
fig_distance.add_trace(go.Bar(x=distance_x, y=distance_y1, name='Daily Avg', text=distance_y1, textposition='inside'))

# 折れ線グラフを追加
fig_distance.add_trace(go.Scatter(x=distance_x, y=distance_y2, mode='lines+markers', yaxis='y2', name='Daily (%)', text=distance_y2, textposition='top right', line=dict(color='yellow')))

# 直線を追加（80%）
fig_distance.add_shape(type='line', x0=0, x1=len(distance_x)-1, y0=80, y1=80, xref='x', yref='y2',
              line=dict(color='red', width=2), name='80%')

# 直線を追加（130%）
fig_distance.add_shape(type='line', x0=0, x1=len(distance_x)-1, y0=130, y1=130, xref='x', yref='y2',
              line=dict(color='red', width=2), name='130%')

# もう一つの折れ線グラフを追加
fig_distance.add_trace(go.Scatter(x=distance_x, y=distance_y3, mode='lines', yaxis='y2', name='Weekly (%)'))

# グラフのレイアウト設定
fig_distance.update_layout(
    title={
        'text': '【Feedback on Team (Distance)】',
        'font': {'size': 20}  # グラフタイトルの文字の大きさを指定します
    },
    xaxis=dict(title='Date'),
    yaxis=dict(title='Daily Avg (m)', side='left'),
    yaxis2=dict(
        title='(%)',
        side='right',
        overlaying='y',
        showgrid=False,
        range=[30, 180]
    )
)




# fig_sprintを作成
# データフレームから必要なデータを取得
sprint_x = sprint_table.columns
sprint_y1 = sprint_table.loc['Daily Avg']
sprint_y2 = sprint_table.loc['Daily (%)'].str.rstrip('%').astype(float)
sprint_y3 = sprint_table.loc['Weekly (%)'].str.rstrip('%').astype(float)

# 2軸グラフの作成
fig_sprint = go.Figure()

# 棒グラフを追加
fig_sprint.add_trace(go.Bar(x=sprint_x, y=sprint_y1, name='Daily Avg', text=sprint_y1, textposition='inside'))

# 折れ線グラフを追加
fig_sprint.add_trace(go.Scatter(x=sprint_x, y=sprint_y2, mode='lines+markers', yaxis='y2', name='Daily (%)', text=sprint_y2, textposition='top right', line=dict(color='yellow')))

# 直線を追加（80%）
fig_sprint.add_shape(type='line', x0=0, x1=len(sprint_x)-1, y0=80, y1=80, xref='x', yref='y2',
              line=dict(color='red', width=2), name='80%')

# 直線を追加（130%）
fig_sprint.add_shape(type='line', x0=0, x1=len(sprint_x)-1, y0=130, y1=130, xref='x', yref='y2',
              line=dict(color='red', width=2), name='130%')

# もう一つの折れ線グラフを追加
fig_sprint.add_trace(go.Scatter(x=sprint_x, y=sprint_y3, mode='lines', yaxis='y2', name='Weekly (%)'))

# グラフのレイアウト設定
fig_sprint.update_layout(
    title={
        'text': '【Feedback on Team (Sprint)】',
        'font': {'size': 20}  # グラフタイトルの文字の大きさを指定します
    },
    xaxis=dict(title='Date'),
    yaxis=dict(title='Daily Avg (Times)', side='left'),
    yaxis2=dict(
        title='(%)',
        side='right',
        overlaying='y',
        showgrid=False,
        range=[30, 180]
    )
)



# fig_accel_allを作成
# データフレームから必要なデータを取得
accel_all_x = accel_all_table.columns
accel_all_y1 = accel_all_table.loc['Daily Avg']
accel_all_y2 = accel_all_table.loc['Daily (%)'].str.rstrip('%').astype(float)
accel_all_y3 = accel_all_table.loc['Weekly (%)'].str.rstrip('%').astype(float)

# 2軸グラフの作成
fig_accel_all = go.Figure()

# 棒グラフを追加
fig_accel_all.add_trace(go.Bar(x=accel_all_x, y=accel_all_y1, name='Daily Avg', text=accel_all_y1, textposition='inside'))

# 折れ線グラフを追加
fig_accel_all.add_trace(go.Scatter(x=accel_all_x, y=accel_all_y2, mode='lines+markers', yaxis='y2', name='Daily (%)', text=accel_all_y2, textposition='top right', line=dict(color='yellow')))

# 直線を追加（80%）
fig_accel_all.add_shape(type='line', x0=0, x1=len(accel_all_x)-1, y0=80, y1=80, xref='x', yref='y2',
              line=dict(color='red', width=2), name='80%')

# 直線を追加（130%）
fig_accel_all.add_shape(type='line', x0=0, x1=len(accel_all_x)-1, y0=130, y1=130, xref='x', yref='y2',
              line=dict(color='red', width=2), name='130%')

# もう一つの折れ線グラフを追加
fig_accel_all.add_trace(go.Scatter(x=accel_all_x, y=accel_all_y3, mode='lines', yaxis='y2', name='Weekly (%)'))

# グラフのレイアウト設定
fig_accel_all.update_layout(
    title={
        'text': '【Feedback on Team (Accel All)】',
        'font': {'size': 20}  # グラフタイトルの文字の大きさを指定します
    },
    xaxis=dict(title='Date'),
    yaxis=dict(title='Daily Avg (Times)', side='left'),
    yaxis2=dict(
        title='(%)',
        side='right',
        overlaying='y',
        showgrid=False,
        range=[30, 180]
    )
)




# fig_decel_allを作成
# データフレームから必要なデータを取得
decel_all_x = decel_all_table.columns
decel_all_y1 = decel_all_table.loc['Daily Avg']
decel_all_y2 = decel_all_table.loc['Daily (%)'].str.rstrip('%').astype(float)
decel_all_y3 = decel_all_table.loc['Weekly (%)'].str.rstrip('%').astype(float)

# 2軸グラフの作成
fig_decel_all = go.Figure()

# 棒グラフを追加
fig_decel_all.add_trace(go.Bar(x=decel_all_x, y=decel_all_y1, name='Daily Avg', text=decel_all_y1, textposition='inside'))

# 折れ線グラフを追加
fig_decel_all.add_trace(go.Scatter(x=decel_all_x, y=decel_all_y2, mode='lines+markers', yaxis='y2', name='Daily (%)', text=decel_all_y2, textposition='top right', line=dict(color='yellow')))

# 直線を追加（80%）
fig_decel_all.add_shape(type='line', x0=0, x1=len(decel_all_x)-1, y0=80, y1=80, xref='x', yref='y2',
              line=dict(color='red', width=2), name='80%')

# 直線を追加（130%）
fig_decel_all.add_shape(type='line', x0=0, x1=len(decel_all_x)-1, y0=130, y1=130, xref='x', yref='y2',
              line=dict(color='red', width=2), name='130%')

# もう一つの折れ線グラフを追加
fig_decel_all.add_trace(go.Scatter(x=decel_all_x, y=decel_all_y3, mode='lines', yaxis='y2', name='Weekly (%)'))

# グラフのレイアウト設定
fig_decel_all.update_layout(
    title={
        'text': '【Feedback on Team (Decel All)】',
        'font': {'size': 20}  # グラフタイトルの文字の大きさを指定します
    },
    xaxis=dict(title='Date'),
    yaxis=dict(title='Daily Avg (Times)', side='left'),
    yaxis2=dict(
        title='(%)',
        side='right',
        overlaying='y',
        showgrid=False,
        range=[30, 180]
    )
)




fig_distance.write_html(f'{desktop_path}/Knows/Training/{folder_name}/Data1.html', auto_open=False)


with open(f'{desktop_path}/Knows/Training/{folder_name}/Data2.html', 'r', encoding='utf-8') as file1:
    html1 = file1.read()

with open(f'{desktop_path}/Knows/Training/{folder_name}/Data3.html', 'r', encoding='utf-8') as file2:
    html2 = file2.read()

combined_html = f"<body>{html1}</body>{html2}"

with open(f'{desktop_path}/Knows/Training/{folder_name}/Data2.html', 'w', encoding='utf-8') as file:
    file.write(combined_html)



fig_sprint.write_html(f'{desktop_path}/Knows/Training/{folder_name}/Data3.html', auto_open=False)

with open(f'{desktop_path}/Knows/Training/{folder_name}/Data2.html', 'r', encoding='utf-8') as file1:
    html1 = file1.read()

with open(f'{desktop_path}/Knows/Training/{folder_name}/Data1.html', 'r', encoding='utf-8') as file2:
    html2 = file2.read()

combined_html = f"<body>{html1}</body>{html2}"

with open(f'{desktop_path}/Knows/Training/{folder_name}/Data2.html', 'w', encoding='utf-8') as file:
    file.write(combined_html)
    
    
    
fig_accel_all.write_html(f'{desktop_path}/Knows/Training/{folder_name}/Data1.html', auto_open=False)

with open(f'{desktop_path}/Knows/Training/{folder_name}/Data2.html', 'r', encoding='utf-8') as file1:
    html1 = file1.read()

with open(f'{desktop_path}/Knows/Training/{folder_name}/Data3.html', 'r', encoding='utf-8') as file2:
    html2 = file2.read()

combined_html = f"<body>{html1}</body>{html2}"

with open(f'{desktop_path}/Knows/Training/{folder_name}/Data2.html', 'w', encoding='utf-8') as file:
    file.write(combined_html)
    
    
    
fig_decel_all.write_html(f'{desktop_path}/Knows/Training/{folder_name}/Data3.html', auto_open=False)

with open(f'{desktop_path}/Knows/Training/{folder_name}/Data2.html', 'r', encoding='utf-8') as file1:
    html1 = file1.read()

with open(f'{desktop_path}/Knows/Training/{folder_name}/Data1.html', 'r', encoding='utf-8') as file2:
    html2 = file2.read()

combined_html = f"<body>{html1}</body>{html2}"

with open(f'{desktop_path}/Knows/Training/{folder_name}/Data2.html', 'w', encoding='utf-8') as file:
    file.write(combined_html)
    

    

with open(f'{desktop_path}/Knows/Training/{folder_name}/Data2.html', 'r', encoding='utf-8') as file1:
    html1 = file1.read()

with open(f'{desktop_path}/Knows/Training/{folder_name}/Data3.html', 'r', encoding='utf-8') as file2:
    html2 = file2.read()

combined_html = f"<body>{html1}</body>{html2}"

with open(f'{desktop_path}/Knows/Training/{folder_name}/Data2.html', 'w', encoding='utf-8') as file:
    file.write(combined_html)
    
    
    
    
    
    
    


# 4つのデータフレームを表示するコード例
html_content = """
<div style="display: flex;">
    <div style="flex: 50%; padding: 10px;">
        <h2>【Distance (m)】</h2>
        {}
    </div>
    <div style="flex: 50%; padding: 10px;">
        <h2>【Sprint (Times)】</h2>
        {}
    </div>
</div>
<div style="display: flex;">
    <div style="flex: 50%; padding: 10px;">
        <h2>【Accel All (Times)】</h2>
        {}
    </div>
    <div style="flex: 50%; padding: 10px;">
        <h2>【Decel All (Times)】</h2>
        {}
    </div>
</div>
""".format(
    distance_table.to_html(),
    sprint_table.to_html(),
    accel_all_table.to_html(),
    decel_all_table.to_html()
)

# HTMLコンテンツをファイルに書き出す
file_path = fr'{desktop_path}/Knows/Training/{folder_name}/Data1.html'

with open(file_path, 'w', encoding='utf-8') as file:
    file.write(html_content)
    
    
    
    
    
    
    
    
    
with open(f'{desktop_path}/Knows/Training/{folder_name}/Data2.html', 'r', encoding='utf-8') as file1:
    html1 = file1.read()

    
with open(f'{desktop_path}/Knows/Training/{folder_name}/Data1.html', 'r', encoding='utf-8') as file2:
    html2 = file2.read()

    
combined_html = f"<body>{html1}</body>{html2}"



with open(f'{desktop_path}/Knows/Training/{folder_name}/index.html', 'w', encoding='utf-8') as file:
    file.write(combined_html)
    
    

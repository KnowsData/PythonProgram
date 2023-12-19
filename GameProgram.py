import warnings
warnings.simplefilter('ignore', FutureWarning)

import pandas as pd
from glob import glob
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import glob
import re
import japanize_matplotlib

print("\n")
print("「'1'」 : 【Feedback from One Game】")
print("「'2'」 : 【Feedback from One Game】 + 【Feedback from Each Game】")
user_choice = input("Enter '1' or '2' → ")



if user_choice == '1':
    
    
    desktop_path = os.path.expanduser('~/Desktop')


    # 変数を使ってフォルダ名を指定
    print("\n")
    print("【Feedback from One Game】")
    folder_name= input("Enter the folder name → ")


    # デスクトップ上の「Knows」フォルダ内のCSVファイルを取得
    filepaths = glob.glob(f'{desktop_path}/Knows/Game/{folder_name}/*.csv')


    # 取得したファイルのリストを表示
    for filepath in filepaths:
        print(filepath)



    # 上で指定したcsvファイルを_dfとして読み込ませる
    _df = pd.read_csv(filepath)


    # _dfから必要な部分だけを抽出し、新しくdfと定義する
    # loc[行,列]で抽出する部分を指定できる（":"の部分はすべてを選択したいときに使える）
    df = _df.loc[:,['Name','Duration_TF','Distance','Sprint','SPD MX',
                    'SPD_D_Z3','SPD_D_Z4','SPD_D_Z5','SPD_D_Z6',
                    'SPD_D_Z1(%)','SPD_D_Z2(%)','SPD_D_Z3(%)','SPD_D_Z4(%)','SPD_D_Z5(%)','SPD_D_Z6(%)',
                    'Accel All','Decel All']]


    #新規にSPD_D_Z3(%)とSPD_D_Z4(%)を計算して追加。その後、不要になったSPD_D_Z5(%)とSPD_D_Z6(%)を削除
    df['SPD_D_Z3(%)'] = df['SPD_D_Z3(%)'] + df['SPD_D_Z4(%)']
    df['SPD_D_Z4(%)'] = df['SPD_D_Z5(%)'] + df['SPD_D_Z6(%)']
    del df ['SPD_D_Z5(%)'], df['SPD_D_Z6(%)']

    df['SPD_D_Z3'] = df['SPD_D_Z3'] + df['SPD_D_Z4']
    df['SPD_D_Z4'] = df['SPD_D_Z5'] + df['SPD_D_Z6']
    del df ['SPD_D_Z5'], df['SPD_D_Z6']


    #'Distance'列が "0" の行を削除
    df = df.drop(df[df['Distance']==0].index)


    #'Distance'の値でデータフレームをソート
    sorted_df = df.sort_values(by='Distance', ascending=False)


    df = sorted_df


    #グラフ用のデータ作成
    data1 = px.bar(df, y=['SPD_D_Z1(%)','SPD_D_Z2(%)','SPD_D_Z3(%)','SPD_D_Z4(%)'], x='Name')
    data2 = px.line(df, y='Distance', x='Name')


    # プロットの初期設定
    fig = make_subplots(specs=[[{"secondary_y": True}]])


    # data1の積み上げグラフを追加
    fig.add_trace(
        go.Bar(x=df['Name'], y=df['SPD_D_Z1(%)'].round(1), name='0~7 km/h(%)'),
        secondary_y=False
    )
    fig.add_trace(
        go.Bar(x=df['Name'], y=df['SPD_D_Z2(%)'].round(1), name='7~14km/h(%)'),
        secondary_y=False
    )
    fig.add_trace(
        go.Bar(x=df['Name'], y=df['SPD_D_Z3(%)'].round(1), name='14~21km/h(%)'),
        secondary_y=False
    )
    fig.add_trace(
        go.Bar(x=df['Name'], y=df['SPD_D_Z4(%)'].round(1), name='21~km/h(%)'),
        secondary_y=False
    )



    # data2の折れ線グラフを追加
    df['Distance_k'] = (df['Distance'] / 1000).round(2).astype(str) + 'k'

    fig.add_trace(
        go.Scatter(x=df['Name'], y=df['Distance'].round(1), name='Distance(m)', 
                   mode='markers+lines+text', textposition='top center', text=df['Distance_k']),
        secondary_y=True
    )

    # 軸ラベルを設定
    fig.update_xaxes(title_text='Name')
    fig.update_yaxes(title_text='SPD_D_Z (%)', secondary_y=False)
    fig.update_yaxes(title_text='Distance (m)', secondary_y=True)


    # 積み上げグラフを上に重ねる
    fig.update_layout(barmode='stack')


    # レイアウトを設定してグラフを表示
    fig.update_layout(
        title={
            'text': "【Feedback on Game】 Distance and Speed of Individual Players",
            'font': {'size': 20}  # タイトルの文字の大きさを指定します
        },
        showlegend=True
    )


    fig.write_html(f'{desktop_path}/Knows/Game/{folder_name}/Data1.html', auto_open=False)






    # 新しいグラフ用のデータ作成
    data3 = px.bar(df, y='SPD MX', x='Name')
    data4 = px.line(df, y=['Sprint', 'Accel All', 'Decel All'], x='Name')


    # プロットの初期設定
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])


    # data3の棒グラフを追加
    fig2.add_trace(
        go.Bar(x=df['Name'], y=df['SPD MX'], name='SPD MAX (km/h)', text=df['SPD MX'], textposition='auto'),
        secondary_y=False
    )


    # data4の折れ線グラフを追加
    fig2.add_trace(
        go.Scatter(x=df['Name'], y=df['Sprint'], name='Sprint (Times)', mode='markers+text', marker=dict(color='yellow', size=30), texttemplate='%{y}'), 
        secondary_y=False
    )
    fig2.add_trace(
        go.Scatter(x=df['Name'], y=df['Accel All'], name='Accel All (Times)', mode='markers+text', marker=dict(color='#EF553B', size=30), texttemplate='%{y}'),
        secondary_y=True
    )
    fig2.add_trace(
        go.Scatter(x=df['Name'], y=df['Decel All'], name='Decel All (Times)', mode='markers+text', marker=dict(color='#19D3F3', size=30), texttemplate='%{y}'),
        secondary_y=True
    )


    # 軸ラベルを設定
    fig2.update_xaxes(title_text='Name')
    fig2.update_yaxes(title_text='SPD MAX、Sprint', secondary_y=False)
    fig2.update_yaxes(title_text='Accel All、Decel All', secondary_y=True)


    # レイアウトを設定してグラフを表示
    fig2.update_layout(
        title={
            'text': "【Feedback on Game】 Actions of Individual Players",
            'font': {'size': 20}  # タイトルの文字の大きさを指定します
        },
        showlegend=True
    )


    fig2.write_html(f'{desktop_path}/Knows/Game/{folder_name}/Data2.html', auto_open=False)





    # 新しいデータフレームを作成
    new_df = pd.DataFrame()
    new_df['Name'] = df['Name']
    new_df['Duration_All'] = df['Duration_TF']
    new_df['Distance(m)'] = df['Distance']
    new_df['Sprint (Times)'] = df['Sprint']
    new_df['SPD MAX(km/h)'] = df['SPD MX']
    new_df['Accel All (Times)'] = df['Accel All']
    new_df['Decel All (Times)'] = df['Decel All']
    new_df['14~21km/h (%)'] = (df['SPD_D_Z3'] / df['Distance']) * 100
    new_df['21~km/h (%)'] = (df['SPD_D_Z4'] / df['Distance']) * 100

    # マーカーを引く関数を作成
    def apply_yellow_highlight_14_21(x):
        if x >= 20:
            return 'background-color: yellow; color: black;'
        else:
            return ''

    def apply_yellow_highlight_21(x):
        if x >= 6:
            return 'background-color: yellow; color: black;'
        else:
            return ''

    # 新しいデータフレームをスタイリング
    styled_df = new_df.style.applymap(apply_yellow_highlight_14_21, subset=['14~21km/h (%)'])
    styled_df = styled_df.applymap(apply_yellow_highlight_21, subset=['21~km/h (%)'])


    # 値を小数点第1まで表示し、その後に「%」マークを表示
    styled_df = styled_df.format({'Distance(m)': '{:.0f}',
                                  'SPD MAX(km/h)': '{:.1f}',
                                  '14~21km/h (%)': '{:.1f}%',
                                  '21~km/h (%)': '{:.1f}%'})

    # インデックス（行番号）を削除
    styled_df = styled_df.hide(axis='index')

    # 枠線を追加
    styled_df = styled_df.set_properties(**{'border': '1px solid black'})

    # 表の外に表示される行名の枠線を追加
    styled_df.set_table_styles([{
        'selector': 'th',
        'props': [('border', '1px solid black')]
    }])

    # HTMLファイルとして保存
    styled_df.to_html(f'{desktop_path}/Knows/Game/{folder_name}/Data3.html', escape=False, index=False)




    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data1.html', 'r', encoding='utf-8') as file1:
        html1 = file1.read()


    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data2.html', 'r', encoding='utf-8') as file2:
        html2 = file2.read()


    combined_html = f"<body>{html1}</body>{html2}"


    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data1.html', 'w', encoding='utf-8') as file:
        file.write(combined_html)




    # 既存のcombined_data.htmlファイルを読み込む
    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data1.html', 'r', encoding='utf-8') as combined_file:
        combined_html = combined_file.read()


    # 新しいHTMLファイル(new_data.html)を読み込む
    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data3.html', 'r', encoding='utf-8') as new_file:
        new_html = new_file.read()


    # 既存のHTMLと新しいHTMLを結合
    combined_html = f"{combined_html}{new_html}"



    # 結合されたHTMLをcombined_data.htmlに書き込む
    with open(f'{desktop_path}/Knows/Game/{folder_name}/index.html', 'w', encoding='utf-8') as combined_file:
        combined_file.write(combined_html)
    
    
    
    
    
    
    
    
    
    
    

    
elif user_choice == '2':
    

    desktop_path = os.path.expanduser('~/Desktop')


    # 変数を使ってフォルダ名を指定
    print("\n")
    print("【Feedback from One Game】")
    folder_name= input("Enter the floder name → ")


    # デスクトップ上の「Knows」フォルダ内のCSVファイルを取得
    filepaths = glob.glob(f'{desktop_path}/Knows/Game/{folder_name}/*.csv')


    # 取得したファイルのリストを表示
    for filepath in filepaths:
        print(filepath)



    # 上で指定したcsvファイルを_dfとして読み込ませる
    _df = pd.read_csv(filepath)


    # _dfから必要な部分だけを抽出し、新しくdfと定義する
    # loc[行,列]で抽出する部分を指定できる（":"の部分はすべてを選択したいときに使える）
    df = _df.loc[:,['Name','Duration_TF','Distance','Sprint','SPD MX',
                    'SPD_D_Z3','SPD_D_Z4','SPD_D_Z5','SPD_D_Z6',
                    'SPD_D_Z1(%)','SPD_D_Z2(%)','SPD_D_Z3(%)','SPD_D_Z4(%)','SPD_D_Z5(%)','SPD_D_Z6(%)',
                    'Accel All','Decel All']]


    #新規にSPD_D_Z3(%)とSPD_D_Z4(%)を計算して追加。その後、不要になったSPD_D_Z5(%)とSPD_D_Z6(%)を削除
    df['SPD_D_Z3(%)'] = df['SPD_D_Z3(%)'] + df['SPD_D_Z4(%)']
    df['SPD_D_Z4(%)'] = df['SPD_D_Z5(%)'] + df['SPD_D_Z6(%)']
    del df ['SPD_D_Z5(%)'], df['SPD_D_Z6(%)']

    df['SPD_D_Z3'] = df['SPD_D_Z3'] + df['SPD_D_Z4']
    df['SPD_D_Z4'] = df['SPD_D_Z5'] + df['SPD_D_Z6']
    del df ['SPD_D_Z5'], df['SPD_D_Z6']


    #'Distance'列が "0" の行を削除
    df = df.drop(df[df['Distance']==0].index)


    #'Distance'の値でデータフレームをソート
    sorted_df = df.sort_values(by='Distance', ascending=False)


    df = sorted_df


    #グラフ用のデータ作成
    data1 = px.bar(df, y=['SPD_D_Z1(%)','SPD_D_Z2(%)','SPD_D_Z3(%)','SPD_D_Z4(%)'], x='Name')
    data2 = px.line(df, y='Distance', x='Name')


    # プロットの初期設定
    fig = make_subplots(specs=[[{"secondary_y": True}]])


    # data1の積み上げグラフを追加
    fig.add_trace(
        go.Bar(x=df['Name'], y=df['SPD_D_Z1(%)'].round(1), name='0~7 km/h(%)'),
        secondary_y=False
    )
    fig.add_trace(
        go.Bar(x=df['Name'], y=df['SPD_D_Z2(%)'].round(1), name='7~14km/h(%)'),
        secondary_y=False
    )
    fig.add_trace(
        go.Bar(x=df['Name'], y=df['SPD_D_Z3(%)'].round(1), name='14~21km/h(%)'),
        secondary_y=False
    )
    fig.add_trace(
        go.Bar(x=df['Name'], y=df['SPD_D_Z4(%)'].round(1), name='21~km/h(%)'),
        secondary_y=False
    )



    # data2の折れ線グラフを追加
    df['Distance_k'] = (df['Distance'] / 1000).round(2).astype(str) + 'k'

    fig.add_trace(
        go.Scatter(x=df['Name'], y=df['Distance'].round(1), name='Distance(m)', 
                   mode='markers+lines+text', textposition='top center', text=df['Distance_k']),
        secondary_y=True
    )

    # 軸ラベルを設定
    fig.update_xaxes(title_text='Name')
    fig.update_yaxes(title_text='SPD_D_Z (%)', secondary_y=False)
    fig.update_yaxes(title_text='Distance (m)', secondary_y=True)


    # 積み上げグラフを上に重ねる
    fig.update_layout(barmode='stack')


    # レイアウトを設定してグラフを表示
    fig.update_layout(
        title={
            'text': "【Feedback on Game】 Distance and Speed of Individual Players",
            'font': {'size': 20}  # タイトルの文字の大きさを指定します
        },
        showlegend=True
    )


    fig.write_html(f'{desktop_path}/Knows/Game/{folder_name}/Data1.html', auto_open=False)







    # 新しいグラフ用のデータ作成
    data3 = px.bar(df, y='SPD MX', x='Name')
    data4 = px.line(df, y=['Sprint', 'Accel All', 'Decel All'], x='Name')


    # プロットの初期設定
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])


    # data3の棒グラフを追加
    fig2.add_trace(
        go.Bar(x=df['Name'], y=df['SPD MX'], name='SPD MAX (km/h)', text=df['SPD MX'], textposition='auto'),
        secondary_y=False
    )


    # data4の折れ線グラフを追加
    fig2.add_trace(
        go.Scatter(x=df['Name'], y=df['Sprint'], name='Sprint (Times)', mode='markers+text', marker=dict(color='yellow', size=30), texttemplate='%{y}'), 
        secondary_y=False
    )
    fig2.add_trace(
        go.Scatter(x=df['Name'], y=df['Accel All'], name='Accel All (Times)', mode='markers+text', marker=dict(color='#EF553B', size=30), texttemplate='%{y}'),
        secondary_y=True
    )
    fig2.add_trace(
        go.Scatter(x=df['Name'], y=df['Decel All'], name='Decel All (Times)', mode='markers+text', marker=dict(color='#19D3F3', size=30), texttemplate='%{y}'),
        secondary_y=True
    )


    # 軸ラベルを設定
    fig2.update_xaxes(title_text='Name')
    fig2.update_yaxes(title_text='SPD MAX、Sprint', secondary_y=False)
    fig2.update_yaxes(title_text='Accel All、Decel All', secondary_y=True)


    # レイアウトを設定してグラフを表示
    fig2.update_layout(
        title={
            'text': "【Feedback on Game】 Actions of Individual Players",
            'font': {'size': 20}  # タイトルの文字の大きさを指定します
        },
        showlegend=True
    )


    fig2.write_html(f'{desktop_path}/Knows/Game/{folder_name}/Data2.html', auto_open=False)





    # 新しいデータフレームを作成
    new_df = pd.DataFrame()
    new_df['Name'] = df['Name']
    new_df['Duration_All'] = df['Duration_TF']
    new_df['Distance(m)'] = df['Distance']
    new_df['Sprint (Times)'] = df['Sprint']
    new_df['SPD MAX(km/h)'] = df['SPD MX']
    new_df['Accel All (Times)'] = df['Accel All']
    new_df['Decel All (Times)'] = df['Decel All']
    new_df['14~21km/h (%)'] = (df['SPD_D_Z3'] / df['Distance']) * 100
    new_df['21~km/h (%)'] = (df['SPD_D_Z4'] / df['Distance']) * 100

    # マーカーを引く関数を作成
    def apply_yellow_highlight_14_21(x):
        if x >= 20:
            return 'background-color: yellow; color: black;'
        else:
            return ''

    def apply_yellow_highlight_21(x):
        if x >= 6:
            return 'background-color: yellow; color: black;'
        else:
            return ''

    # 新しいデータフレームをスタイリング
    styled_df = new_df.style.applymap(apply_yellow_highlight_14_21, subset=['14~21km/h (%)'])
    styled_df = styled_df.applymap(apply_yellow_highlight_21, subset=['21~km/h (%)'])


    # 値を小数点第1まで表示し、その後に「%」マークを表示
    styled_df = styled_df.format({'Distance(m)': '{:.0f}',
                                  'SPD MAX(km/h)': '{:.1f}',
                                  '14~21km/h (%)': '{:.1f}%',
                                  '21~km/h (%)': '{:.1f}%'})

    # インデックス（行番号）を削除
    styled_df = styled_df.hide(axis='index')

    # 枠線を追加
    styled_df = styled_df.set_properties(**{'border': '1px solid black'})

    # 表の外に表示される行名の枠線を追加
    styled_df.set_table_styles([{
        'selector': 'th',
        'props': [('border', '1px solid black')]
    }])

    # HTMLファイルとして保存
    styled_df.to_html(f'{desktop_path}/Knows/Game/{folder_name}/Data3.html', escape=False, index=False)




    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data1.html', 'r', encoding='utf-8') as file1:
        html1 = file1.read()


    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data2.html', 'r', encoding='utf-8') as file2:
        html2 = file2.read()


    combined_html = f"<body>{html1}</body>{html2}"


    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data1.html', 'w', encoding='utf-8') as file:
        file.write(combined_html)




    # 既存のcombined_data.htmlファイルを読み込む
    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data1.html', 'r', encoding='utf-8') as combined_file:
        combined_html = combined_file.read()


    # 新しいHTMLファイル(new_data.html)を読み込む
    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data3.html', 'r', encoding='utf-8') as new_file:
        new_html = new_file.read()


    # 既存のHTMLと新しいHTMLを結合
    combined_html = f"{combined_html}{new_html}"


    # 結合されたHTMLをcombined_data.htmlに書き込む
    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data1.html', 'w', encoding='utf-8') as combined_file:
        combined_file.write(combined_html)





    



    def load_csv_and_sum(folder_path):
        file_list = os.listdir(folder_path)
        data = {}

        for file in file_list:
            if file.endswith('.csv'):
                match = re.search(r'_(\d{8})_', file)
                if match:
                    date = match.group(1)
                    formatted_date = f"{date[:4]}/{date[4:6]}/{date[6:8]}"
                    file_path = os.path.join(folder_path, file)
                    df = pd.read_csv(file_path)
                    sum_values = df[['Distance', 'Sprint', 'Accel All', 'Decel All', 'Accel_Z2', 'Accel_Z3', 'Decel_Z2', 'Decel_Z3', 'SPD_D_Z3', 'SPD_D_Z4', 'SPD_D_Z5', 'SPD_D_Z6', 'SPD_D_Z3(%)', 'SPD_D_Z4(%)', 'SPD_D_Z5(%)', 'SPD_D_Z6(%)']].sum()
                    data[formatted_date] = sum_values
    
        return pd.DataFrame(data).T

    def load_csv_and_mean(folder_path):
        file_list = os.listdir(folder_path)
        data = {}

        for file in file_list:
            if file.endswith('.csv'):
                match = re.search(r'_(\d{8})_', file)
                if match:
                    date = match.group(1)
                    formatted_date = f"{date[:4]}/{date[4:6]}/{date[6:8]}"
                    file_path = os.path.join(folder_path, file)
                    df = pd.read_csv(file_path)
                    # 平均計算時にセル内の0を無視する
                    df.replace(0, pd.NA, inplace=True)  # 0をNaNに変換
                    mean_values = df[['Distance', 'Sprint', 'Accel All', 'Decel All', 'Accel_Z2', 'Accel_Z3', 'Decel_Z2', 'Decel_Z3', 'SPD_D_Z3', 'SPD_D_Z4', 'SPD_D_Z5', 'SPD_D_Z6', 'SPD_D_Z3(%)', 'SPD_D_Z4(%)', 'SPD_D_Z5(%)', 'SPD_D_Z6(%)']].mean(skipna=True)
                    data[formatted_date] = mean_values

        return pd.DataFrame(data).T

    def create_plot(df, plot_title):
        df['14~21km/h (m)'] = df['SPD_D_Z3'] + df['SPD_D_Z4']
        df['21~km/h (m)'] = df['SPD_D_Z5'] + df['SPD_D_Z6']
        df['14~21km/h (%)'] = df['SPD_D_Z3(%)'] + df['SPD_D_Z4(%)']
        df['21~km/h (%)'] = df['SPD_D_Z5(%)'] + df['SPD_D_Z6(%)']
        df.drop(['SPD_D_Z3', 'SPD_D_Z4', 'SPD_D_Z5', 'SPD_D_Z6', 'SPD_D_Z3(%)', 'SPD_D_Z4(%)', 'SPD_D_Z5(%)', 'SPD_D_Z6(%)'], axis=1, inplace=True)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        for column in df.columns:
            if column not in ['SPD_D_Z3', 'SPD_D_Z4', 'SPD_D_Z5', 'SPD_D_Z6']:
                text_values = df[column].apply(lambda x: int(x))
                fig.add_trace(go.Bar(x=df.index, y=df[column], name=column, text=text_values, textposition='auto', showlegend=False))

        fig.update_layout(
            title={
                'text': plot_title,
                'font': {
                    'size': 20  # タイトルのフォントサイズを20に設定
                }
            },
            xaxis=dict(title='Date'),
            barmode='group',
            legend=dict(x=1.02, y=1)
        )

        return fig

    user_name = os.getlogin()
    folder_path = rf'{desktop_path}\Knows\Game'

    print("\n")
    print("【Feedback from Each Game】")
    folders = []
    while True:
        folder = input("Enter the folder name (Type 'end' to finish) → ")
        if folder.lower() == 'end':
            break
        folders.append(folder)

    combined_df_sum = pd.DataFrame()
    combined_df_mean = pd.DataFrame()

    for folder in folders:
        selected_folder = os.path.join(folder_path, folder)
        df_sum = load_csv_and_sum(selected_folder)
        df_mean = load_csv_and_mean(selected_folder)
        combined_df_sum = pd.concat([combined_df_sum, df_sum])
        combined_df_mean = pd.concat([combined_df_mean, df_mean])

    fig_sum = create_plot(combined_df_sum, '【Comparison of Team Total Values】')
    fig_mean = create_plot(combined_df_mean, '【Comparison of Team Average Values】')


    renamed_columns = {
        'Distance': 'Distance (m)',
        'Sprint': 'Sprint (Times)',
        'Accel All': 'Accel All (Times)',
        'Decel All': 'Decel All (Times)',
        'Accel_Z2': 'Accel_Z2 (Times)',
        'Accel_Z3': 'Accel_Z3 (Times)',
        'Decel_Z2': 'Decel_Z2 (Times)',
        'Decel_Z3': 'Decel_Z3 (Times)'
    }


    dropdown_buttons_sum = []
    for column in combined_df_sum.columns:
        if column not in ['SPD_D_Z3', 'SPD_D_Z4', 'SPD_D_Z5', 'SPD_D_Z6', 'SPD_D_Z3(%)', 'SPD_D_Z4(%)', 'SPD_D_Z5(%)', 'SPD_D_Z6(%)', '14~21km/h (%)', '21~km/h (%)']:
            dropdown_buttons_sum.append(
                dict(label=renamed_columns.get(column, column), method="update", args=[{"visible": [col == column for col in combined_df_sum.columns]}])
            )

    dropdown_buttons_mean = []
    for column in combined_df_mean.columns:
        if column not in ['SPD_D_Z3', 'SPD_D_Z4', 'SPD_D_Z5', 'SPD_D_Z6', 'SPD_D_Z3(%)', 'SPD_D_Z4(%)', 'SPD_D_Z5(%)', 'SPD_D_Z6(%)']:
            dropdown_buttons_mean.append(
                dict(label=renamed_columns.get(column, column), method="update", args=[{"visible": [col == column for col in combined_df_mean.columns]}])
            )
        elif column in ['14~21km/h (%)', '21~km/h (%)']:
            dropdown_buttons_mean.append(
                dict(label=renamed_columns.get(column, column), method="update", args=[{"visible": [col == column for col in combined_df_mean.columns]}])
            )


    initial_visibility_sum = [False] * len(combined_df_sum.columns)
    initial_visibility_sum[0] = True

    initial_visibility_mean = [False] * len(combined_df_mean.columns)
    initial_visibility_mean[0] = True

    fig_sum.update_traces(visible='legendonly')
    fig_sum.update_traces(visible=True, selector=dict(name=combined_df_sum.columns[0]))

    fig_mean.update_traces(visible='legendonly')
    fig_mean.update_traces(visible=True, selector=dict(name=combined_df_mean.columns[0]))

    fig_sum.update_layout(
        updatemenus=[
            dict(
                buttons=dropdown_buttons_sum,
                direction="down",
                showactive=True,
                x=1.02,
                xanchor='left',
                y=1
            ),
        ]
    )

    fig_mean.update_layout(
        updatemenus=[
            dict(
                buttons=dropdown_buttons_mean,
                direction="down",
                showactive=True,
                x=1.02,
                xanchor='left',
                y=1
            ),
        ]
    )

    max_values_sum = combined_df_sum.max()
    max_values_mean = combined_df_mean.max()

    for i, col in enumerate(combined_df_sum.columns):
        fig_sum.update_yaxes(range=[0, max_values_sum[i] * 1.2], secondary_y=False, selector=dict(name=col))

    for i, col in enumerate(combined_df_mean.columns):
        fig_mean.update_yaxes(range=[0, max_values_mean[i] * 1.2], secondary_y=False, selector=dict(name=col))

    fig_sum.write_html(f"{desktop_path}/Knows/Game/{folder_name}/Data2.html", auto_open=False)
    fig_mean.write_html(f"{desktop_path}/Knows/Game/{folder_name}/Data3.html", auto_open=False)


    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data1.html', 'r', encoding='utf-8') as file1:
        html1 = file1.read()


    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data2.html', 'r', encoding='utf-8') as file2:
        html2 = file2.read()


    combined_html = f"<body>{html1}</body>{html2}"


    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data1.html', 'w', encoding='utf-8') as file:
        file.write(combined_html)

        

    
    

    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data1.html', 'r', encoding='utf-8') as file1:
        html1 = file1.read()


    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data3.html', 'r', encoding='utf-8') as file2:
        html2 = file2.read()


    combined_html = f"<body>{html1}</body>{html2}"


    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data1.html', 'w', encoding='utf-8') as file:
        file.write(combined_html)
    
    
    
    
    
    
    
    
    # CSVファイルから新しいデータフレームを作成する関数
    def create_dataframe_from_csv(file_path):
        df = pd.read_csv(file_path)

        # 必要な列の抽出
        required_columns = ['Name', 'Distance', 'Sprint', 'SPD_D_Z3', 'SPD_D_Z4', 'SPD_D_Z5', 'SPD_D_Z6', 'SPD_D_Z3(%)', 'SPD_D_Z4(%)', 'SPD_D_Z5(%)']
        df = df[required_columns]

        # 新しい列の追加
        df['14~21km/h (m)'] = df['SPD_D_Z3'] + df['SPD_D_Z4']
        df['21~km/h (m)'] = df['SPD_D_Z5'] + df['SPD_D_Z6']
        df['14~21km/h (%)'] = df['SPD_D_Z3(%)'] + df['SPD_D_Z4(%)']
        df['21~km/h (%)'] = df['SPD_D_Z4(%)'] + df['SPD_D_Z5(%)']

        return df[['Name', 'Distance', 'Sprint', '14~21km/h (m)', '21~km/h (m)', '14~21km/h (%)', '21~km/h (%)']]

    # CSVファイルからそれぞれ新しいデータフレームを作成する
    dataframes = {}

    for folder in folders:
        folder_dir = os.path.join(folder_path, folder)
        file_list = os.listdir(folder_dir)

        for file in file_list:
            if file.endswith('.csv'):
                file_path = os.path.join(folder_dir, file)
                df = create_dataframe_from_csv(file_path)

                # CSVファイル名から日付を抽出して指定された形式に変換
                file_name = file.split('.')[0]
                date_parts = file_name.split('_')[1]  # '20230506'の部分を取得
                formatted_date = f"{date_parts[:4]}/{date_parts[4:6]}/{date_parts[6:]}"  # 'YYYY/MM/DD'の形式に変換

                # 辞書にデータフレームを格納
                dataframes[formatted_date] = df


    
    
    
    def create_individual_dataframes(dataframes):
        individual_dataframes = {}  # 個別のデータフレームを格納するための辞書
    
        # 各日付のデータフレームから「Name」の値を抽出し、個別のデータフレームを作成
        for date, df in dataframes.items():
            for _, row in df.iterrows():
                name = row['Name']
                if name not in individual_dataframes:
                    # 新しいデータフレームを作成し、データを追加
                    individual_dataframes[name] = pd.DataFrame(columns=['Distance', 'Sprint', '14~21km/h (m)', '21~km/h (m)', '14~21km/h (%)', '21~km/h (%)'])

                # データを追加
                individual_dataframes[name] = pd.concat([individual_dataframes[name], pd.DataFrame({
                    'Distance': [row['Distance']],
                    'Sprint': [row['Sprint']],
                    '14~21km/h (m)': [row['14~21km/h (m)']],
                    '21~km/h (m)': [row['21~km/h (m)']],
                    '14~21km/h (%)': [row['14~21km/h (%)']],
                    '21~km/h (%)': [row['21~km/h (%)']]
                })], ignore_index=True)
    
        # 行名を日付名に変更する
        for name, df in individual_dataframes.items():
            df.index = [date for date in dataframes.keys() if name in dataframes[date]['Name'].values]

        return individual_dataframes

    # 各日付のデータフレームから個別のデータフレームを作成
    individual_dfs = create_individual_dataframes(dataframes)


    
    
    
    
    # 6つのデータフレームをそれぞれの列名に基づいてリストにまとめる
    distance_data = [df['Distance'].tolist() for _, df in individual_dfs.items()]
    sprint_data = [df['Sprint'].tolist() for _, df in individual_dfs.items()]
    speed_14_data = [df['14~21km/h (m)'].tolist() for _, df in individual_dfs.items()]
    speed_21_data = [df['21~km/h (m)'].tolist() for _, df in individual_dfs.items()]
    percentage_14_data = [df['14~21km/h (%)'].tolist() for _, df in individual_dfs.items()]
    percentage_21_data = [df['21~km/h (%)'].tolist() for _, df in individual_dfs.items()]

    # データフレームの行名を取得
    x_values = [list(df.index) for _, df in individual_dfs.items()]

    # カスタムカラーパレットの作成
    custom_palette = px.colors.cyclical.mygbm * 20 # 必要な数だけ色を拡張

    # サブプロットの作成
    fig = make_subplots(rows=3, cols=2, subplot_titles=['「Distance」', '「Sprint」', '「14~21km/h (m)」', '「21~km/h (m)」', '「14~21km/h (%)」', '「21~km/h (%)」'])

    # サブプロットに集合棒グラフを追加
    for i, df_name in enumerate(individual_dfs):
        fig.add_trace(go.Bar(x=x_values[i], y=distance_data[i], name=df_name, marker=dict(color=custom_palette[i])), row=1, col=1)
        fig.add_trace(go.Bar(x=x_values[i], y=sprint_data[i], name=df_name, marker=dict(color=custom_palette[i])), row=1, col=2)
        fig.add_trace(go.Bar(x=x_values[i], y=speed_14_data[i], name=df_name, marker=dict(color=custom_palette[i])), row=2, col=1)
        fig.add_trace(go.Bar(x=x_values[i], y=speed_21_data[i], name=df_name, marker=dict(color=custom_palette[i])), row=2, col=2)
        fig.add_trace(go.Bar(x=x_values[i], y=percentage_14_data[i], name=df_name, marker=dict(color=custom_palette[i])), row=3, col=1)
        fig.add_trace(go.Bar(x=x_values[i], y=percentage_21_data[i], name=df_name, marker=dict(color=custom_palette[i])), row=3, col=2)

    # レイアウトの調整
    fig.update_layout(title_text="【Comparison of Individual Players Values】", title_font_size=20)
    fig.update_xaxes(title_text="Date")

    # 縦軸のタイトルを変更
    fig.update_yaxes(title_text="(m)", row=1, col=1)
    fig.update_yaxes(title_text="(Times)", row=1, col=2)
    fig.update_yaxes(title_text="(m)", row=2, col=1)
    fig.update_yaxes(title_text="(m)", row=2, col=2)
    fig.update_yaxes(title_text="(%)", row=3, col=1)
    fig.update_yaxes(title_text="(%)", row=3, col=2)

    # ドロップダウンメニューの作成
    buttons = [{"label": "All", "method": "update", "args": [{"visible": [True] * len(fig.data)}]}]
    for df_name in individual_dfs:
        visible_traces = [True if trace.name == df_name else False for trace in fig.data]
        buttons.append({"label": df_name, "method": "update", "args": [{"visible": visible_traces}]})

    # グラフエリアのレイアウトを更新してドロップダウンメニューを配置
    fig.update_layout(updatemenus=[{"buttons": buttons, "direction": "down", "showactive": True, "x": 1.05, "xanchor": "left", "y": 1.00, "yanchor": "top"}])

    # 凡例の非表示
    fig.update_layout(showlegend=False)


    # グラフをHTMLファイルとして保存
    fig.write_html(f"{desktop_path}/Knows/Game/{folder_name}/Data2.html", auto_open=False)    
    
    
    

    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data1.html', 'r', encoding='utf-8') as file1:
        html1 = file1.read()


    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data2.html', 'r', encoding='utf-8') as file2:
        html2 = file2.read()


    combined_html = f"<body>{html1}</body>{html2}"


    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data1.html', 'w', encoding='utf-8') as file:
        file.write(combined_html)


        

        
        
        
        

        

    # CSVファイルから新しいデータフレームを作成する関数
    def create_dataframe_from_csv(file_path):
        df = pd.read_csv(file_path)

        # 必要な列の抽出
        required_columns = ['Name', 'Accel All', 'Decel All', 'Accel_Z2', 'Accel_Z3', 'Decel_Z2', 'Decel_Z3']
        df = df[required_columns]

        return df[['Name', 'Accel All', 'Decel All', 'Accel_Z2', 'Accel_Z3', 'Decel_Z2', 'Decel_Z3']]

    # CSVファイルからそれぞれ新しいデータフレームを作成する
    dataframes = {}

    for folder in folders:
        folder_dir = os.path.join(folder_path, folder)
        file_list = os.listdir(folder_dir)

        for file in file_list:
            if file.endswith('.csv'):
                file_path = os.path.join(folder_dir, file)
                df = create_dataframe_from_csv(file_path)

                # CSVファイル名から日付を抽出して指定された形式に変換
                file_name = file.split('.')[0]
                date_parts = file_name.split('_')[1]  # '20230506'の部分を取得
                formatted_date = f"{date_parts[:4]}/{date_parts[4:6]}/{date_parts[6:]}"  # 'YYYY/MM/DD'の形式に変換

                # 辞書にデータフレームを格納
                dataframes[formatted_date] = df


        
        
        
        
        
    def create_individual_dataframes(dataframes):
        individual_dataframes = {}  # 個別のデータフレームを格納するための辞書

        # 各日付のデータフレームから「Name」の値を抽出し、個別のデータフレームを作成
        for date, df in dataframes.items():
            for _, row in df.iterrows():
                name = row['Name']
                if name not in individual_dataframes:
                    # 新しいデータフレームを作成し、データを追加
                    individual_dataframes[name] = pd.DataFrame(columns=['Accel All', 'Decel All', 'Accel_Z2', 'Accel_Z3', 'Decel_Z2', 'Decel_Z3'])

                # データを追加
                individual_dataframes[name] = pd.concat([individual_dataframes[name], pd.DataFrame({
                    'Accel All': [row['Accel All']],
                    'Decel All': [row['Decel All']],
                    'Accel_Z2': [row['Accel_Z2']],
                    'Accel_Z3': [row['Accel_Z3']],
                    'Decel_Z2': [row['Decel_Z2']],
                    'Decel_Z3': [row['Decel_Z3']]
                })], ignore_index=True)

        # 行名を日付名に変更する
        for name, df in individual_dataframes.items():
            df.index = [date for date in dataframes.keys() if name in dataframes[date]['Name'].values]

        return individual_dataframes

    # 各日付のデータフレームから個別のデータフレームを作成
    individual_dfs = create_individual_dataframes(dataframes)


        
        

        
        
        
    # 6つのデータフレームをそれぞれの列名に基づいてリストにまとめる
    Accel_All_data = [df['Accel All'].tolist() for _, df in individual_dfs.items()]
    Decel_All_data = [df['Decel All'].tolist() for _, df in individual_dfs.items()]
    Accel_Z2_data = [df['Accel_Z2'].tolist() for _, df in individual_dfs.items()]
    Accel_Z3_data = [df['Accel_Z3'].tolist() for _, df in individual_dfs.items()]
    Decel_Z2_data = [df['Decel_Z2'].tolist() for _, df in individual_dfs.items()]
    Decel_Z3_data = [df['Decel_Z3'].tolist() for _, df in individual_dfs.items()]

    # データフレームの行名を取得
    x_values = [list(df.index) for _, df in individual_dfs.items()]

    # カスタムカラーパレットの作成
    custom_palette = px.colors.cyclical.mygbm * 20 # 必要な数だけ色を拡張

    # サブプロットの作成
    fig = make_subplots(rows=3, cols=2, subplot_titles=['「Accel All」', '「Decel All」', '「Accel_Z2」', '「Accel_Z3」', '「Decel_Z2」', '「Decel_Z3」'])

    # サブプロットに集合棒グラフを追加
    for i, df_name in enumerate(individual_dfs):
        fig.add_trace(go.Bar(x=x_values[i], y=Accel_All_data[i], name=df_name, marker=dict(color=custom_palette[i])), row=1, col=1)
        fig.add_trace(go.Bar(x=x_values[i], y=Decel_All_data[i], name=df_name, marker=dict(color=custom_palette[i])), row=1, col=2)
        fig.add_trace(go.Bar(x=x_values[i], y=Accel_Z2_data[i], name=df_name, marker=dict(color=custom_palette[i])), row=2, col=1)
        fig.add_trace(go.Bar(x=x_values[i], y=Accel_Z3_data[i], name=df_name, marker=dict(color=custom_palette[i])), row=2, col=2)
        fig.add_trace(go.Bar(x=x_values[i], y=Decel_Z2_data[i], name=df_name, marker=dict(color=custom_palette[i])), row=3, col=1)
        fig.add_trace(go.Bar(x=x_values[i], y=Decel_Z3_data[i], name=df_name, marker=dict(color=custom_palette[i])), row=3, col=2)

    # レイアウトの調整
    fig.update_xaxes(title_text="Date")

    # 縦軸のタイトルを変更
    fig.update_yaxes(title_text="(Times)", row=1, col=1)
    fig.update_yaxes(title_text="(Times)", row=1, col=2)
    fig.update_yaxes(title_text="(Times)", row=2, col=1)
    fig.update_yaxes(title_text="(Times)", row=2, col=2)
    fig.update_yaxes(title_text="(Times)", row=3, col=1)
    fig.update_yaxes(title_text="(Times)", row=3, col=2)

    # ドロップダウンメニューの作成
    buttons = [{"label": "All", "method": "update", "args": [{"visible": [True] * len(fig.data)}]}]
    for df_name in individual_dfs:
        visible_traces = [True if trace.name == df_name else False for trace in fig.data]
        buttons.append({"label": df_name, "method": "update", "args": [{"visible": visible_traces}]})

    # グラフエリアのレイアウトを更新してドロップダウンメニューを配置
    fig.update_layout(updatemenus=[{"buttons": buttons, "direction": "down", "showactive": True, "x": 1.00, "xanchor": "left", "y": 1.00, "yanchor": "top"}])

    # 凡例の非表示
    fig.update_layout(showlegend=False)


    # グラフをHTMLファイルとして保存
    fig.write_html(f"{desktop_path}/Knows/Game/{folder_name}/Data3.html", auto_open=False)
    
    
    
    
    
    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data1.html', 'r', encoding='utf-8') as file1:
        html1 = file1.read()


    with open(f'{desktop_path}/Knows/Game/{folder_name}/Data3.html', 'r', encoding='utf-8') as file2:
        html2 = file2.read()


    combined_html = f"<body>{html1}</body>{html2}"


    with open(f'{desktop_path}/Knows/Game/{folder_name}/index.html', 'w', encoding='utf-8') as file:
        file.write(combined_html)    
        
        
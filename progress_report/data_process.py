import datetime
import os
from pathlib import Path

import japanize_matplotlib  # noqa: F401
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

import seaborn as sns; sns.set()  # noqa: E702


def get_jst() -> datetime.datetime:
    """呼び出された時刻の日本時刻を返す関数

    Returns:
        datetime.datetime: 呼び出された時刻の日本時刻
    """
    diff_from_utc = 9
    jst = datetime.datetime.utcnow() + datetime.timedelta(hours=diff_from_utc)
    return jst


def find_proper_csv(book_name: str, csv_dir: str) -> str:
    """入力された本の名前をもつcsvファイル(本の名前.csv)があるか確認して、
    あればそのファイルへのパスを、
    なければ空の「本の名前.csv」を作りそこへのパスを返す関数

    Args:
        book_name (str): 登録された本の名前
        csv_dir (str): 進捗管理をしているcsvファイルを一括で管理してるディレクトリへのパス

    Returns:
        str: 本の名前.csv へのパス
    """
    csvs_list = os.listdir(csv_dir)
    books_name_list = [csv[:-4] for csv in csvs_list]

    if book_name in books_name_list:
        csv_path = str(Path(csv_dir) / "{}.csv".format(book_name))
    else:
        empty_df = pd.DataFrame(columns=["日時", "どこまで進んだか"])
        csv_path = str(Path(csv_dir) / "{}.csv".format(book_name))
        empty_df.to_csv(csv_path, index=False)
    return csv_path


def write_in_csv(progress: int, csv_path: str) -> pd.DataFrame:
    """進捗管理csvファイルに更新情報を書き込む関数

    Args:
        progress (int): 進捗を累計どこまでうんだのか(ex. 何ページまで読んだのか)
        csv_path (str): 進捗管理csvファイルの所定の位置へのファイルパス

    Returns:
        pd.DataFrame: 更新後のcsvファイルのDataFrame版
    """
    dataframe = pd.read_csv(csv_path)
    time = get_jst()
    new_row = pd.DataFrame([{"日時": time, "どこまで進んだか": progress}])
    dataframe_update = pd.concat([dataframe, new_row], ignore_index=True, join="inner")
    dataframe_update.to_csv(csv_path)
    return dataframe_update


def draw_graph(dataframe_update: pd.DataFrame, graph_path_dir: str) -> None:
    """特定のディレクトリに、進捗状況の折れ線グラフが"年-月-日.png"の形で保存して保存先のパスを返す関数

    Args:
        dataframe_update (pd.DataFrame): 更新後のcsvファイルのDataFrame版
        graph_path_dir (str): 進捗状況の可視化グラフが格納されるディレクトリへのパス

    Returns:
        str: グラフの保存先へパス
    """
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(dataframe_update["日時"].apply(lambda x: str(x)).str[5:10], dataframe_update["どこまで進んだか"])
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=1, maxticks=10))

    graph_path_dir = Path(graph_path_dir)
    time_str = str(get_jst)[:10]
    result_graph_path = str(graph_path_dir / "{}.png".format(time_str))
    plt.savefig(result_graph_path)
    return result_graph_path

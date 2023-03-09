from fastapi import FastAPI
from fastapi.responses import FileResponse

from progress_report.data_process import (draw_graph,  # noqa: E501
                                          find_proper_csv, write_in_csv)


def process_data(book_name: str, progress: int, csv_dir: str, graph_dir: str) -> str:  # noqa: E501
    """入力情報を用いて進捗管理を行うcsvファイルを更新して格納し、
    進捗状況を可視化したグラフを作成し格納する関数

    Args:
        book_name (str): 読んでいる本の名前
        progress (int): 何ページまで読んだか
        csv_dir (str): 進捗管理を行うcsvファイルの格納ディレクトリ先
        graph_dir (str): 進捗状況を可視化したファイルの格納ディレクトリ先

    Returns:
        str: 進捗状況を可視化したファイルへのファイルパス
    """
    csv_path = find_proper_csv(book_name, csv_dir)
    progress_dataframe = write_in_csv(progress, csv_path)
    result_graph_path = draw_graph(progress_dataframe, graph_dir)
    return result_graph_path


router = FastAPI()


@router.post("/progress_report")
async def progress_report_api(
        book_name: str,
        progress: int,
        ) -> FileResponse:
    """APi叩いて読んでいる本の名前と何ページまで読んだかを入力すると進捗状況のグラフが返ってくる関数

    Args:
        book_name (str): 読んでいる本の名前
        progress (int): 何ページまで読んだか

    Returns:
        FileResponse: 進捗結果のグラフ
    """
    csv_dir = "progress_report_csv"
    graph_dir = "progress_report_graph"
    result_graph_path = process_data(book_name, progress, csv_dir, graph_dir)

    return FileResponse(path=result_graph_path, filename=result_graph_path)

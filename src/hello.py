import os  # OS依存の機能を利用するモジュールをインポート
import sys  # システム固有のパラメータや関数を利用するモジュールをインポート
import sqlite3  # SQLiteデータベースを利用するモジュールをインポート

def main() -> int:  # メイン関数を定義。戻り値は整数型
    base_dir = os.path.dirname(os.path.abspath(__file__))  # スクリプトの絶対パスからディレクトリパスを取得
    db_path = os.path.join(base_dir, "master.db")  # ディレクトリパスとDBファイル名を結合してパスを作成

    if len(sys.argv) != 3:  # コマンドライン引数の数が3つ（スクリプト名+2つの引数）でないか確認
        return 2  # 引数エラーを示す終了コード2を返して関数を終了

    code = sys.argv[1]  # 1つ目の引数を商品コードとして変数に格納
    qty_str = sys.argv[2]  # 2つ目の引数を数量（文字列）として変数に格納

    try:  # 例外が発生する可能性のあるブロックを開始
        qty = int(qty_str)  # 数量の文字列を整数に変換
    except Exception:  # 例外（整数に変換不可等）が発生した場合の処理
        print("ERROR,QTY_NOT_INT")  # エラーメッセージ（数量が整数でない）を出力
        return 0  # 正常終了扱い（業務エラー）として0を返す

    try:  # DB操作のトライブロック開始
        con = sqlite3.connect(db_path)  # データベースに接続
        cur = con.cursor()  # カーソルオブジェクトを作成
        cur.execute("SELECT price FROM items WHERE code = ?", (code,))  # 変数codeとDBのcodeを照合し、合致した行のpriceを特定
        row = cur.fetchone()  # 上で実行したSQLの検索結果を1行取得し、変数rowに格納
        con.close()  # データベース接続を閉じる
    except Exception:  # DB操作中に例外が発生した場合
        return 1  # システムエラーとして終了コード1を返す

    if row is None:  # 取得した行が空（該当商品なし）の場合
        print("ERROR,ITEM_NOT_FOUND")  # エラーメッセージ（商品が見つからない）を出力
        return 0  # 業務エラーとして0を返す

    price = row[0]  # 取得した行の最初のカラム（価格）を変数に格納

    try:  # 価格の型変換トライブロック開始
        price_int = int(price)  # 価格を整数に変換
    except Exception:  # 型変換に失敗した場合
        print("ERROR,PRICE_NOT_INT")  # エラーメッセージ（価格が整数でない）を出力
        return 0  # 業務エラーとして0を返す

    total = price_int * qty  # 合計金額を計算
    print(f"OK,{price_int},{total}")  # 成功メッセージと単価、合計金額を出力
    return 0  # 正常終了として0を返す

if __name__ == "__main__":  # スクリプトとして直接実行された場合
    raise SystemExit(main())  # main関数を実行し、その戻り値で終了する

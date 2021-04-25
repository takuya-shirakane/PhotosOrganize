import glob
import shutil
import pathlib
import piexif
import re
import datetime
import sys

JPG = "JPG"
NIKON = "NEF"
SONY = "ARW"


class PhotosOrganize:
    def __init__(self, input_dir, output_dir):
        args = sys.argv
        if len(args) != 4:
            print("引数を指定してください")
            sys.exit(1)

        self.input_path = input_dir

        # outputのディレクトリが存在しない場合は作成する
        self.check_directory(output_dir)

        # 出力先のディレクトリを作成
        self.output_path = f"{output_dir}/{args[3]}"

        # 開始日時と終了日時を設定
        self.date_args = {"year": 0, "month": 1, "day": 2, "hour": 3, "minites": 4}
        self.start_time = self.change_date(args[1])
        self.finish_time = self.change_date(args[2])

    def change_date(self, date):
        """
        引数で受け取った日時をdatetime型に変更する

        args:
            date:datetime型に変換する日時
        return:
            date:datetime型に変換した日時
        """
        # データの情報を分割
        date_info = re.split("[\-\s:]", date)

        if len(date_info) < 4:
            # 分割して多い場合は不正のため終了
            print("日付を正しい形で指定してください。")
            sys.exit(1)

        # datetime型に変換
        change_date = datetime.datetime(
            year=int(date_info[self.date_args["year"]]),
            month=int(date_info[self.date_args["month"]]),
            day=int(date_info[self.date_args["day"]]),
            hour=int(date_info[self.date_args["hour"]]),
        )
        return change_date

    def copy_photos(self, data_type):
        """
        指定した拡張子の写真をコピーする

        args:
            data_type:拡張子の種類
        """
        # 写真のリストを作成
        photo_list = sorted(glob.glob(f"{self.input_path}/*.{data_type}"))

        if data_type == JPG and not photo_list:
            photo_list = sorted(glob.glob(f"{self.input_path}/*.{data_type.lower()}"))

        if not photo_list:
            print(f"「.{data_type}」の画像は存在しません。")
            return

        # ディレクトリが存在しない場合は作成する
        output_dir = self.output_path + data_type
        self.check_directory(output_dir)

        count = 0

        for photo in photo_list:
            # 写真のデータを取得
            img = piexif.load(photo)

            # 撮影日時を取得
            shooting_date = self.change_date(img["Exif"][36867].decode())

            start_check = (shooting_date - self.start_time).days >= 0
            finish_check = (shooting_date - self.finish_time).days < 0
            if start_check and finish_check:
                # 撮影日時が指定した日時内であればコピーを実施
                count += 1
                shutil.copy(photo, output_dir)
                print(f"「{photo}」を「{output_dir}」にコピーしました。")
            elif count != 0:
                # countが1以上であればループを抜ける
                break

        print(f"「.{data_type}」の画像を{count}枚コピーしました。")

    def check_directory(self, path):
        """
        ディレクトリが存在するかをチェックし、存在しない場合は作成する

        args:
            type:ディレクトリのパス
        """
        path = pathlib.Path(path)
        if not path.exists():
            # ディレクトリが存在しない場合は作成
            path.mkdir()


def main():
    # パスを指定
    input_dir = ""
    output_dir = ""
    photo = PhotosOrganize(input_dir, output_dir)

    # 拡張子のリスト
    photo_types = [JPG, NIKON, SONY]

    # 拡張子毎にコピーを実施
    for photo_type in photo_types:
        photo.copy_photos(photo_type)


if __name__ == "__main__":
    print("start")
    main()
    print("finish")

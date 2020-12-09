import glob
import shutil
import pathlib
import piexif
import re
import datetime
import sys

JPG = "jpg"
NIKON = "NEF"
SONY = "ARW"


class PhotosOrganize:
    def __init__(self, title, input, output):
        args = sys.argv
        if len(args) != 3:
            print("引数を指定してください")
            sys.exit(1)

        self.input_path = input

        # outputのディレクトリが存在しない場合は作成する
        self.check_directory(output)

        # 出力先のディレクトリを作成
        self.output_path = output + "/" + title
        self.check_directory(self.output_path)

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
        date_info = re.split("[\-\s:]", date)
        if len(date_info) < 4:
            print("日付を正しい形で指定してください。")
            sys.exit(1)
        change_date = datetime.datetime(
            year=int(date_info[self.date_args["year"]]),
            month=int(date_info[self.date_args["month"]]),
            day=int(date_info[self.date_args["day"]]),
            hour=int(date_info[self.date_args["hour"]]),
        )
        return change_date

    def copy_photos(self, type):
        """
        指定した拡張子の写真をコピーする

        args:
            type:拡張子の種類
        """
        # 写真のリストを作成
        photo_list = glob.glob(self.input_path + "/*." + type)

        if not photo_list:
            print(f"「.{type}」の画像は存在しません。")
            return

        output_dir = self.output_path + "/" + type

        # ディレクトリが存在しない場合は作成する
        self.check_directory(output_dir)

        # コピーを実施
        for photo in photo_list:
            img = piexif.load(photo)
            shooting_date = self.change_date(img["Exif"][36867].decode())

            start_check = (shooting_date - self.start_time).days > 0
            finish_check = (shooting_date - self.finish_time).days < 0
            if start_check and finish_check:
                shutil.copy(photo, output_dir)
                print(f"「{photo}」を「{output_dir}」にコピーしました。")
            else:
                print(f"「{photo}」は指定された日付の範囲外です。")

        print(f"「.{type}」の画像のコピーが完了しました。")

    def check_directory(self, path):
        """
        ディレクトリが存在するかをチェックし、存在しない場合は作成する

        args:
            type:ディレクトリのパス
        """
        path = pathlib.Path(path)
        if not path.exists():
            path.mkdir()


def main():
    # パスを指定
    title = "20201204"
    input = ""
    output = ""
    photo = PhotosOrganize(title, input, output)

    # 拡張子のリスト
    type_list = [JPG, NIKON, SONY]

    # 拡張子毎にコピーを実施
    for type in type_list:
        photo.copy_photos(type)


if __name__ == "__main__":
    print("start")
    main()
    print("finish")

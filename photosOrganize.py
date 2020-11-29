import glob
import shutil
import pathlib


class PhotosOrganize:
    def __init__(self, title, input, output):
        self.input_path = input

        # outputのディレクトリが存在しない場合は作成する
        self.check_directory(output)

        # 出力先のディレクトリを作成
        self.output_path = output + "/" + title
        self.check_directory(self.output_path)

    def copy_photos(self, type):
        """
        指定した拡張子の写真をコピーする

        Parameters:
        ----------
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
            shutil.copy(photo, output_dir)
            print(f"「{photo}」を画像を「{output_dir}」にコピーしました。")

        print(f"「.{type}」の画像のコピーが完了しました。")

    def check_directory(self, path):
        """
        ディレクトリが存在するかをチェックし、存在しない場合は作成する

        Parameters:
        ----------
        type:ディレクトリのパス
        """
        path = pathlib.Path(path)
        if not path.exists():
            path.mkdir()


def main():
    # パスを指定
    title = "フォトウォーク"
    input = ""
    output = ""
    photo = PhotosOrganize(title, input, output)

    # 拡張子のリスト
    type_list = ["jpg", "NEF"]

    # 拡張子毎にコピーを実施
    for type in type_list:
        photo.copy_photos(type)


if __name__ == "__main__":
    print("start")
    main()
    print("finish")

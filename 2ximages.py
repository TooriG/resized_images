import os
from PIL import Image, PngImagePlugin
import argparse
from datetime import datetime
import shutil

def resize_image(image_path, output_path, metadata, factor=2):
    with Image.open(image_path) as image:
        # 新しいサイズを計算
        new_size = (image.width * factor, image.height * factor)
        # 画像をリサイズ
        resized_image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # メタデータをPngInfoオブジェクトに変換する
        pnginfo = PngImagePlugin.PngInfo()
        for k, v in metadata.items():
            # メタデータがテキストの場合にのみ追加
            if isinstance(v, str):
                pnginfo.add_text(k, v)

        # リサイズされた画像を保存
        resized_image.save(output_path, "PNG", pnginfo=pnginfo)

def copy_structure_and_resize_images(input_folder, output_folder, factor=2):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(input_folder):
        # 出力用のサブディレクトリを作成
        relative_path = os.path.relpath(root, input_folder)
        output_subfolder = os.path.join(output_folder, relative_path)
        if not os.path.exists(output_subfolder):
            os.makedirs(output_subfolder)

        for file in files:
            input_path = os.path.join(root, file)
            output_path = os.path.join(output_subfolder, file)

            # ファイルがPNG画像の場合、リサイズ
            if file.lower().endswith('.png'):
                # 画像を開いてメタデータを取得
                with Image.open(input_path) as image:
                    metadata = image.info
                resize_image(input_path, output_path, metadata, factor)
            # 画像以外のファイルはそのままコピー
            else:
                shutil.copy2(input_path, output_path)

            print(f"Processed: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Copy folder structure and resize PNG images.')
    parser.add_argument('input_folder', type=str, help='Input folder containing files to process.')
    args = parser.parse_args()

    # 現在時刻を含むユニークなアウトプットフォルダ名を生成
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_folder = f"{args.input_folder}_resized_{timestamp}"

    copy_structure_and_resize_images(args.input_folder, output_folder)
    print("All files have been copied and images resized in the new folder.")

"""
Tools to manipulate path locations
"""


class FileTools:

    @staticmethod
    def change_dir(name_new_dir, path_current_dir):
        new_dir = path_current_dir.split("/")
        new_dir[-1] = name_new_dir
        new_dir = "/".join(new_dir)
        return new_dir

    @staticmethod
    def df_to_csv(df, path):
        try:
            # Save analysed excel to CSV
            df.to_csv(path, index=False, encoding='utf-8', )
            print(f"File successfully saved at {path}")
        except FileNotFoundError:
            print(f"The directory '{path}' does not exist. Please create it before running the code.")
        except Exception as e:
            print(e)



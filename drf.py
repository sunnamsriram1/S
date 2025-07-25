import os
import shutil

def delete_restored_files(directory):
    deleted = 0
    for root, dirs, files in os.walk(directory, topdown=False):
        # Delete matching files
        for name in files:
            if name.endswith('_restored'):
                path = os.path.join(root, name)
                os.remove(path)
                print(f'🗑️ Deleted file: {path}')
                deleted += 1
        # Delete matching folders
        for name in dirs:
            if name.endswith('_restored'):
                path = os.path.join(root, name)
                shutil.rmtree(path)
                print(f'🗑️ Deleted folder: {path}')
                deleted += 1
    print(f'\n✅ Done! Total deleted: {deleted}')

if __name__ == '__main__':
    delete_restored_files('.')

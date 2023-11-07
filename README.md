# google_image_download
Downloads images from Google search results based on a specified search query string, such as "cute kittens."


set up .venv
install black and isort for formatting
add file/folders to the gitignore
add very simple test



### Building the python package

The package can be build and installed with symlinks by doing the following:

```bash
cd google_iamge_download
pip install -e .
python setup.py sdist --formats=gztar
```

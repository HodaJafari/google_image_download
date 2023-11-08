# google_image_download
Downloads images from Google search results based on a specified search query string, such as "cute kittens."

#### Python environment

In order to keep the development process tidy, you should use a virtual environment when installing
application-specific packages. There are multiple ways to set up virtual environments (e.g. using
Pipenv), but the example below shows how you can do this using the native tools:

```bash
cd google_image_download
python3 -m venv .venv
```

**NOTE**: Never commit your virtual environment to git, as this adds a lot of uneccesary files.

Then install requirements on your virtual environment:

```bash
source .venv/bin/activate
```

Then run the following commands to install all requirements for local:

```bash
pip install -r requirements.txt

```

To deactivate the virtual environment you just need to run the following commands:

```bash
deactivate
```
### Linting
For formatting our code we use *black* and *isort* packages.

### Building the python package

The package can be build and installed with symlinks by doing the following:

```bash
cd google_iamge_download
pip install -e .
python setup.py sdist --formats=gztar
```

## Database
Before running the project create a PostgreSQL database on your local with a table name  *google_images* and with a column name *file_path*. Because we are running this query in the program:

```bash
INSERT INTO public.google_images(file_path) VALUES ($1);
```

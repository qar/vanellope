# VANELLOPE

> A personal blog site solution designed to be deployed with a minimal effort.

## Setup

1. Install the latest version of Docker
2. Enter the base directory and run `make run_dev`
3. Open `http://localhost:9900` in web browser (manually refresh may required)
4. In order to preview on another port, change `DEV_PORT` in Makefile.variable`, repeat Step-2


## Add database table

1. Add new table schema in `create_table_sql` in config.py
2. Restart application will initiate the new table
3. Add new query interface in `da`, which means `DataAccess`

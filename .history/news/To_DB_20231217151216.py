{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 39,
   "metadata": {},
   "outputs": [],
   "source": [
    "import json\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import datetime\n",
    "import sqlalchemy\n",
    "import pickle\n",
    "from sqlalchemy import create_engine, VARCHAR\n",
    "host = 'localhost'\n",
    "port = \"3306\"\n",
    "user = 'root'\n",
    "pwd = 'test123'\n",
    "database_name = 'sentiment_texts'\n",
    "con = create_engine('mysql+pymysql://'+user+':'+pwd+'@'+host+':'+port+'/'+database_name)\n",
    "\n",
    "def onStop(json_file):\n",
    "    json_file.close()\n",
    "    \n",
    "def get_item(filename):\n",
    "    # file_path = 'C:/Users/USER/Desktop/sentiment_Text/news/texts/2023121521_anue_友達.json'\n",
    "    json_file = open(f\"texts/{filename}\", 'r', encoding=\"utf-8\", errors=\"replace\")\n",
    "    dict_posts = json.load(json_file)\n",
    "    onStop(json_file)\n",
    "    return dict_posts\n",
    "\n",
    "search = \"顯示器\"\n",
    "filename = '2023121713_anue_顯示器.json'\n",
    "path = f'C:/Users/USER/Desktop/sentiment_Text/news/texts/{filename}'\n",
    "dict_posts = get_item(filename)\n",
    "\n",
    "urls = pd.DataFrame(dict_posts.keys(), columns = [\"url\"])\n",
    "times_contents = pd.DataFrame(dict_posts.values(), columns=[\"time\", \"content\"])\n",
    "data = pd.merge(urls, times_contents, left_index=True, right_index=True)\n",
    "\n",
    "max_date = datetime.datetime.strptime(max(data['time']), \"%Y/%m/%d %H:%M\").strftime(\"%Y%m%d\")\n",
    "min_date = datetime.datetime.strptime(min(data['time']), \"%Y/%m/%d %H:%M\").strftime(\"%Y%m%d\")\n",
    "f\"anue_{search}_{max_date}to{min_date}\"\n",
    "table_name = f\"anue_{search}_{str(max_date)}to{str(min_date)}\"\n",
    "data.to_sql(table_name, con=con, if_exists='replace')\n",
    "\n",
    "# load data from database\n",
    "sql_query = f'SELECT * FROM {table_name}'\n",
    "# Use pandas to read the data directly into a DataFrame\n",
    "df = pd.read_sql(sql_query, con)\n",
    "# Close the MySQL connection\n",
    "# con.close()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

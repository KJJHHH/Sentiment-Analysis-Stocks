# A. Scrape
- Work in computer
- Web including udn, ltn, ptt, dccard, etc
- Store time, title, text, link with dict to dataframe type in sql by "sentiment_text{media}{indsutry}{keyword}"
- Select "from date" and "latest date"\
**!!!!Learn: hadoop, ...**
# B. Scores
- Scores sentiment
    -
    ### ⏰Description
    1. from text compute emotion for each date.
    2. predict next day's return with predicted emotion
    ### ⏰Notices
    🎼 ***Inputs: media name, industry, and keywords***\
    🎼 ***Data: Dictionary from pickle***\
    🎼 ***output: sentiment with returns***

- Predicting
    -
    - Too slow, config to google colab. Refers as
    - https://www.strongdm.com/docs/admin/resources/datasources/mysql\
    - https://colab.research.google.com/github/GoogleCloudPlatform/cloud-sql-python-connector/blob/main/samples/notebooks/mysql_python_connector.ipynb#scrollTo=fVz5zhvZ1mM3
    - **Mainly on jacoblifenice@gmail.com**
    ```
    ⚡ Note: haven't connect colab to sql, so train and backtest on colab with fix time range of data, predict on base.
    ```
    -  ### Ways to compute scores
        - Connect to SQL
        - Group by same date, concat all text in same date 
        - Switch to dict and set dict keys be date
        - Iterate  the following 
            - In each date split all text in the day by \r
            - Translate to Eng
            - Compute scores for neutral, pos, neg with Finbert 
            https://github.com/yuanbit/FinBERT-QA-notebooks
            - Define score func with neu, pos, neg
            - Return title and text scores for each date
        - Dataframe with Date, title sscores, text scores
- Errors refers
    -
    1. The size of tensor a (605) must match the size of tensor b (512) at non-singleton dimension 1\
    https://www.google.com/search?q=list+to+jsson&rlz=1C1GCEA_enTW920TW920&oq=list+to+jsson&aqs=chrome..69i57j35i39i650j0i67i650l3j0i131i433i512j0i67i650j0i512j0i67i650l2.3924j0j7&sourceid=chrome&ie=UTF-8
    2. list ot json\
    https://sparkbyexamples.com/python/convert-python-list-to-json/
# C. Evaluation
    - Plot
    - backtesting

# D. Refers
### NLP
### Finbert
https://github.com/yuanbit/FinBERT-QA-notebooks
https://github.com/ProsusAI/finBERT/blob/master/notebooks/finbert_training.ipynb
### colab
colab gpu?
https://sites.research.google/trc/about/
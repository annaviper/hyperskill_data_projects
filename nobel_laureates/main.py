import pandas as pd
import os
import requests
import sys
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if 'Nobel_laureates.json' not in os.listdir('../Data'):
        sys.stderr.write("[INFO] Dataset is loading.\n")
        url = "https://www.dropbox.com/s/m6ld4vaq2sz3ovd/nobel_laureates.json?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/Nobel_laureates.json', 'wb').write(r.content)
        sys.stderr.write("[INFO] Loaded.\n")

    """STAGE 1"""
    # write your code here
    df = pd.read_json('/Users/anna/PycharmProjects/Nobel Laureates/Nobel Laureates/Data/Nobel_laureates.json')

    duplicated_rows = df[df.duplicated()]
    if len(duplicated_rows) > 0:
        print(True)
    else:
        print(False)

    df2 = df.dropna(subset=['gender'])

    df3 = df2.reset_index(drop=True)

    print(df3[['country', 'name']].head(20).to_dict())

    """STAGE 2"""
    df = df3.copy()
    df['place_of_birth_clean'] = df['place_of_birth'].apply(lambda x: x.split(',')[-1].strip() if isinstance(x, str) and ',' in x else None)

    df['born_in'] = df['born_in'].replace('', None)
    df['born_in'] = df['born_in'].fillna(df['place_of_birth_clean'])
    df = df.dropna(subset=['born_in']).reset_index(drop=True)

    replacement_dict = {
        'US': 'USA',
        'United States': 'USA',
        'U.S.': 'USA',
        'United Kingdom': 'UK'
    }
    df['born_in'] = df['born_in'].replace(replacement_dict)
    # print(list(df['born_in']))

    """STAGE 3"""
    df['year_of_birth'] = df['date_of_birth'].str.extract(r'(\d{4})').astype(int)
    df['age_of_winning'] = df['year'] - df['year_of_birth'].astype(int)
    # print(df['year_of_birth'].to_list(), "\n", df['age_of_winning'].to_list())

    """STAGE 4"""
    country_counts = df['born_in'].value_counts()
    df['born_in'] = df['born_in'].apply(lambda x: 'Other countries' if country_counts[x] < 25 else x)

    colors = ['blue', 'orange', 'red', 'yellow', 'green', 'pink', 'brown', 'cyan', 'purple']
    to_explode = ['UK', 'France', 'Russia', 'Austria', 'Canada', 'Poland']
    explode = [0.08 if country in to_explode else 0 for country in df['born_in'].unique()]


    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return '{p:.2f}%\n({v:d})'.format(p=pct, v=val)
        return my_autopct


    # Create the pie chart
    plt.figure(figsize=(12, 12))
    plt.pie(
        df['born_in'].value_counts(),
        labels=df['born_in'].value_counts().index,
        colors=colors,
        explode=explode,
        autopct=make_autopct(df['born_in'].value_counts()),  # {:.2f}%\n({:.0f}
        startangle=140
    )
    plt.title('Distribution of Nobel Laureates by Country')
    plt.show()

    """STAGE 5"""
    df.category = df.category.replace('', None)
    df = df.dropna(subset=['category'])

    pivot_table = df.pivot_table(
        index='category',
        columns='gender',
        values='country',
        aggfunc='count'
    )

    categories = pivot_table.index.tolist()
    female_counts = pivot_table['female'].tolist()
    male_counts = pivot_table['male'].tolist()

    width = 0.4
    x = np.arange(len(categories))

    fig, ax = plt.subplots(figsize=(10, 10))
    plt.figure(figsize=(10, 10))

    plt.bar(x - 0.2, male_counts, width=0.4, label='Males', color='blue')
    plt.bar(x + 0.2, female_counts, width=0.4, label='Females', color='crimson')

    plt.xticks(ticks=x, labels=categories)
    plt.xlabel('Category', fontsize=14)

    plt.ylabel('Nobel Laureates Count', fontsize=14)
    plt.title('The total count of male and female Nobel Prize winners by categories', fontsize=20)

    plt.yticks(np.arange(0, 201, 25))  # Stop at 200
    plt.legend()
    plt.show()

    """STAGE 6"""
    plt.figure(figsize=(10, 10))

    all_data = df['age_of_winning']
    data = [df[df['category'] == cat]['age_of_winning'] for cat in df['category'].unique()]

    combined_data = data + [all_data]

    plt.boxplot(combined_data, labels=categories + ['All categories'], widths=0.6, showmeans=True)

    plt.ylabel('Age of Obtaining the Nobel Prize', fontsize=14)
    plt.xlabel('Category', fontsize=14)
    plt.title('Distribution of Ages by category', fontsize=20)
    plt.show()
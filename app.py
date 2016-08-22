from flask import Flask, request, redirect, render_template, send_file
import pandas as pd
import os


def create_app():
    app=Flask(__name__)
    return app

app = create_app()

"""
@app.route("/", methods=['GET', 'POST'])
def index():
    print "running"
    myDFs, rooms, years = create_pivots('Traffic Report Sample_gus.xlsx', 'Traffic Data')
    if request.method == 'POST':
        if request.form['btn'] == 'display':
            yr = request.form['year']
            rm = request.form['room']
            print yr, rm
            for myDF in myDFs:
                if myDF['room'] == int(rm) and myDF['year'] == int(yr):
                    myFiltDF = myDF['df']
                    return render_template('index.html', myFoo=myFiltDF.to_html(), years=years, rooms=rooms)
            return render_template('index.html', years=years, rooms=rooms, no_data_msg="No Data for that Unit & Year")
    return render_template('index.html', years=years, rooms=rooms)
"""

@app.route("/", methods=['GET', 'POST'])
def test():
    df = pd.read_excel('Traffic Report Sample_gus.xlsx')
    filt_df = df[df['Year'] == 2016]
    pivot_df = pd.pivot_table(filt_df, values='nameid', columns='Action', index=['rmpropid','mrktname'], aggfunc='count')
    pivot_df.reset_index(inplace=True)
    pivot_df.index.name = None
    cdf = pd.pivot_table(df, columns='Action', index=['rmpropid', 'leasagid'], values='nameid', aggfunc='count', margins=True)
    #cdf.columns = [' '.join(col).strip() for col in cdf.columns.values]
    cdf.reset_index(inplace=True)
    return render_template('report.html', myDF=pivot_df.to_html(), cdf=cdf.to_html())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=int(port), debug=True)
    #app.run(debug=True)
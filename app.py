from flask import Flask, request, redirect, render_template, send_file
import pandas as pd
import os


def create_app():
    app=Flask(__name__)
    return app

app = create_app()

@app.route("/", methods=['GET', 'POST'])
def test():
    df = pd.read_excel('Traffic Report Sample_gus.xlsx')
    df_2015 = df[df['Year'] == 2015]
    df_2016 = df[df['Year'] == 2016]
    props_2015 = df_2015.rmpropid.tolist()
    props_2016 = df_2016.rmpropid.tolist()
    years = set(df.Year.tolist())
    if request.method == 'POST':
        if request.form['btn'] == 'display':
            prop = request.form['room']
            year = request.form['year']
            year_df = df[df['Year'] == int(year)]
            filt_df = year_df[year_df['rmpropid'] == int(prop)]
            pivot_df = pd.pivot_table(filt_df, values='nameid', columns='Action', index='mrktname', aggfunc='count')
            cdf = pd.pivot_table(filt_df, columns='Action', index='leasagid', values='nameid', aggfunc='count', margins=True)
            tdf = pd.pivot_table(filt_df, values='nameid', index='Month', aggfunc='count')
            try:
                t_out = tdf.to_html()
            except AttributeError:
                t_out = tdf.to_frame().to_html()
            sdf = pd.pivot_table(filt_df, values='nameid', index='mrktname', aggfunc='count')
            try:
                s_out = sdf.to_html()
            except AttributeError:
                s_out = sdf.to_frame().to_html()
            return render_template('report.html', myDF=pivot_df.to_html(), cdf=cdf.to_html(), tdf=t_out, sdf=s_out, prop=prop, year=year)
    return render_template('index.html', years=years, props_2015=props_2015, props_2016=props_2016)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=int(port), debug=True)
    #app.run(debug=True)
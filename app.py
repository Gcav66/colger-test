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
    props_2015 = list(set(df_2015.rmpropid))
    props_2016 = list(set(df_2016.rmpropid))
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
        if request.form['btn'] == 'download':
            prop = request.form['room']
            year = request.form['year']
            year_df = df[df['Year'] == int(year)]
            filt_df = year_df[year_df['rmpropid'] == int(prop)]
            pdf = pd.pivot_table(filt_df, values='nameid', columns='Action', index='mrktname', aggfunc='count')
            cdf = pd.pivot_table(filt_df, columns='Action', index='leasagid', values='nameid', aggfunc='count', margins=True)
            tdf = pd.pivot_table(filt_df, values='nameid', index='Month', aggfunc='count')
            sdf = pd.pivot_table(filt_df, values='nameid', index='mrktname', aggfunc='count')
            xls_name = "Borger_" + str(prop) + "_" + str(year) + "_Report.xlsx"
            writer = pd.ExcelWriter(xls_name)
            pdf.to_excel(writer, 'Sheet1')
            cdf.to_excel(writer, 'Sheet2')
            try:
                tdf.to_excel(writer, 'Sheet3')
            except AttributeError:
                tdf.to_frame().to_excel(writer, 'Sheet3')
            try:
                sdf.to_excel(xls_name, 'Sheet4')
            except AttributeError:
                sdf.to_frame().to_excel(writer, 'Sheet4')
            writer.save()
            return send_file(xls_name, as_attachment=True)
    return render_template('index.html', years=years, props_2015=props_2015, props_2016=props_2016)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=int(port), debug=True)
    #app.run(debug=True)
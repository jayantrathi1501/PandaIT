from flask import Flask, request, render_template,redirect,url_for,send_file,Response
import io
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index1', methods=['POST'])
def index1():
    return render_template('index1.html')

@app.route('/index2', methods=['POST'])
def index2():
    return render_template('index2.html')

@app.route('/upload1', methods=['POST'])
def upload1():
    uploaded_file = request.files['file']
    if uploaded_file.filename.endswith('.csv'):
        global df
        df = pd.read_csv(uploaded_file)
        global col
        col = df.columns
        return render_template('uploaded1.html')
        #return render_template('index.html',ans=g.df["birth_year"].sum())
    else:
        ans = 'Invalid file format. Please upload a CSV file.'
        return render_template('index1.html',ans=ans)

@app.route('/upload2', methods=['POST'])
def upload2():
    uploaded_file = request.files['file']
    if uploaded_file.filename.endswith('.csv'):
        global df
        df = pd.read_csv(uploaded_file)
        global col
        col = df.columns
        return render_template('uploaded2.html',col=col)
        #return render_template('index.html',ans=g.df["birth_year"].sum())
    else:
        ans = 'Invalid file format. Please upload a CSV file.'
        return render_template('index2.html',ans=ans)

@app.route('/back', methods=['POST'])
def back():
    return redirect(url_for('index'))

@app.route('/Sum', methods=['POST'])
def Sum():
    global df
    column_name = request.form.get("column_name_sum", "")
    if column_name == "":
        return render_template('uploaded1.html', Sum_ans="Column name not provided")
    try:
        total_sum = df[column_name].sum()
    except KeyError:
        return render_template('uploaded1.html', Sum_ans="Invalid column name")
    return render_template('uploaded1.html', Sum_ans=total_sum)

@app.route('/mean', methods=['POST'])
def mean():
    global df
    column_name = request.form.get("column_name_mean", "")
    if column_name == "":
        return render_template('uploaded1.html', Mean_ans="Column name not provided")
    try:
        total_sum = df[column_name].mean()
    except KeyError:
        return render_template('uploaded1.html', Mean_ans="Invalid column name")
    return render_template('uploaded1.html', Mean_ans=total_sum)

@app.route('/median', methods=['POST'])
def median():
    global df
    column_name = request.form.get("column_name_median", "")
    if column_name == "":
        return render_template('uploaded1.html', Median_ans="Column name not provided")
    try:
        total_sum = df[column_name].median()
    except KeyError:
        return render_template('uploaded1.html', Median_ans="Invalid column name")
    return render_template('uploaded1.html', Median_ans=total_sum)

@app.route('/mode', methods=['POST'])
def mode():
    global df
    column_name = request.form.get("column_name_mode", "")
    if column_name == "":
        return render_template('uploaded1.html', Mode_ans="Column name not provided")
    try:
        total_sum = df[column_name].mode()
    except KeyError:
        return render_template('uploaded1.html', Mode_ans="Invalid column name")
    return render_template('uploaded1.html', Mode_ans=total_sum)


@app.route('/avg', methods=['POST'])
def avg():
    global df
    column_name = request.form.get("column_name_avg", "")
    if column_name == "":
        return render_template('uploaded1.html', avg_ans="Column name not provided")
    try:
        total_sum = df[column_name].sum() / len(df[column_name])
    except KeyError:
        return render_template('uploaded1.html', avg_ans="Invalid column name")
    return render_template('uploaded1.html', avg_ans=total_sum)


@app.route('/add_index', methods=['POST'])
def add_index():
    global df
    global col
    if "S.no" not in col:
        df.insert(0, 'S.no', range(1, len(df) + 1))
        col = df.columns
        return render_template('uploaded1.html',ans_index="Index added" )
    else:
        return render_template('uploaded1.html', ans_index="Index already added")

@app.route('/total_rows', methods=['POST'])
def total_rows():
    global df
    global col
    col=df.columns
    return render_template('uploaded1.html', t_r=len(df[col[0]]))

@app.route('/Unique_r', methods=['POST'])
def Unique_r():
    global df
    column_name = request.form.get("column_name_uni_r", "")
    if column_name == "":
        return render_template('uploaded1.html', Uni_rows="Column name not provided")
    try:
        unique_values = len(df[column_name].unique())
    except KeyError:
        return render_template('uploaded1.html', Uni_rows="Invalid column name")
    return render_template('uploaded1.html', Uni_rows=unique_values)

@app.route('/Unique_r_val', methods=['POST'])
def Unique_r_val():
    global df
    column_name = request.form.get("column_name_uni_r_val", "")
    if column_name == "":
        return render_template('uploaded1.html', Uni_rows_error="Column name not provided")
    try:
        unique_values = df[column_name].unique()
    except KeyError:
        return render_template('uploaded1.html', Uni_rows_error="Invalid column name")
    return render_template('uploaded1.html', row=unique_values)

@app.route('/top_row', methods=['POST'])
def top_row():
    global df
    no_of_row = request.form.get("no_of_row", "")
    if no_of_row == "":
        return render_template('uploaded1.html', error="No. of rows not provided")
    try:
        n=int(no_of_row)
        d=df.head(n)
        data = d.values
    except KeyError:
        return render_template('uploaded1.html', error="Invalid column name")
    return render_template('uploaded1.html', headings=col,data=data)

@app.route('/bottom_row', methods=['POST'])
def bottom_row():
    global df
    no_of_row = request.form.get("no_of_row", "")
    if no_of_row == "":
        return render_template('uploaded1.html', error="No. of rows not provided")
    try:
        n=int(no_of_row)
        d=df.tail(n)
        data = d.values
    except KeyError:
        return render_template('uploaded1.html', error="Invalid column name")
    return render_template('uploaded1.html', headings=col,data=data)

@app.route('/all_row1', methods=['POST'])
def all_row1():
    global df
    try:
        col=df.columns       
        data = df.values
    except KeyError:
        return render_template('uploaded1.html', error="Invalid column name")
    return render_template('uploaded1.html', headings=col,data=data)

@app.route('/all_row2', methods=['POST'])
def all_row2():
    global df
    try:
        col=df.columns       
        data = df.values
    except KeyError:
        return render_template('uploaded2.html', error="Invalid column name")
    return render_template('uploaded2.html', headings=col,data=data)

@app.route('/download2', methods=['POST'])
def download2():
    global df
    csv_data = df.to_csv(index=False)
    response = Response(io.StringIO(csv_data),mimetype="text/csv",headers={"Content-disposition": "attachment; filename=data.csv"})
    return response

@app.route('/download1', methods=['POST'])
def download1():
    global df
    csv_data = df.to_csv(index=False)
    response = Response(io.StringIO(csv_data),mimetype="text/csv",headers={"Content-disposition": "attachment; filename=data.csv"})
    return response

@app.route('/select_column2', methods=['POST'])
def select_column2():
    if request.method == 'POST':
        # Retrieve the values of submitted checkboxes
        submitted_checkboxes = request.form.getlist('my_checkbox')
    else:
        return render_template('uploaded2.html')
    
    try:
        global df
        df=df[submitted_checkboxes]
        global col
        col = df.columns
        return render_template('uploaded2.html',ans=f"The submitted checkboxes are: {', '.join(submitted_checkboxes)}")
    except KeyError:
        return render_template('uploaded2.html', error="Invalid columns selected")

@app.route('/all_col2', methods=['POST'])
def all_col2():
    global col
    col = df.columns
    return render_template('uploaded2.html',col=col)

@app.route('/all_col1', methods=['POST'])
def all_col1():
    global col
    col = df.columns
    return render_template('uploaded1.html',col=col)

@app.route('/del_col2', methods=['POST'])
def del_col2():
    global df
    column_name = request.form.get("col_name_del", "")
    if column_name == "":
        return render_template('uploaded2.html', error="Column name not provided")
    try:
        df = df.drop(column_name, axis=1)
        global col
        col = df.columns
    except KeyError:
        return render_template('uploaded2.html', error="Invalid column name")
    return render_template('uploaded2.html',ans=column_name+" deleted")


@app.route('/filter_col_str2', methods=['POST'])
def filter_col_str2():
    global df
    column_name = request.form.get("col_name_filter", "")
    column_val = request.form.get("col_value_list", "")
    if column_name == "" or column_val == "":
        print(column_name,column_val )
        return render_template('uploaded2.html', error="Column name or value not provided")
    try:
        column_val=column_val.split(",")
        df= df[df[column_name].isin(column_val)]
    except KeyError:
        return render_template('uploaded2.html', error="Invalid column name or value ")
    return render_template('uploaded2.html')

@app.route('/filter_col_int2', methods=['POST'])
def filter_col_int2():
    global df
    column_name = request.form.get("col_name_filter", "")
    column_val = request.form.get("col_value_list", "")
    if column_name == "" or column_val == "":
        return render_template('uploaded2.html', error="Column name or value not provided")
    try:
        column_val = list(map(float,column_val.strip().split(",")))
        df= df[df[column_name].isin(column_val)]
    except KeyError:
        return render_template('uploaded2.html', error="Invalid column name or value ")
    return render_template('uploaded2.html')

@app.route('/filter_col_opp2', methods=['POST'])
def filter_col_opp2():
    global df
    column_name = request.form.get("col_name_filter", "")
    column_val = int(request.form.get("col_value_list", ""))
    column_opp=request.form.get("col_opp")
    if column_name == "" or column_val == "" or column_opp == "":
        return render_template('uploaded2.html', error="Column name or value not provided")
    try:
        if column_opp=="<":
            df= df[df[column_name] < column_val]
        elif column_opp==">":
            df= df[df[column_name] > column_val]
    except KeyError:
        return render_template('uploaded2.html', error="Invalid column name or value ")
    return render_template('uploaded2.html')

@app.route('/check_emp', methods=['POST'])
def check_emp():
    global df
    column_name = request.form.get("column_name_check_emp", "")
    if column_name == "":
        return render_template('uploaded1.html', error="Column name or value not provided")
    try:
        has_none = df[column_name].isna().any()
    except KeyError:
        return render_template('uploaded1.html', error="Invalid column name or value ")
    if has_none:
        return render_template('uploaded1.html',ans_check_emp="Yes, None or empty value found")
    else:
        return render_template('uploaded1.html',ans_check_emp="No, None or Empty value not found")
    
@app.route('/remove_na', methods=['POST'])
def remove_na():
    global df
    column_name = request.form.get("column_name_remove_na", "")
    if column_name == "":
        return render_template('uploaded1.html', ans_remove_na="Column name or value not provided")
    try:
        df = df.dropna(subset=[column_name])
        return render_template('uploaded1.html',ans_remove_na="Removed null values")
    except KeyError:
        return render_template('uploaded1.html', ans_remove_na="Invalid column name or value ")
    
@app.route('/fill_na', methods=['POST'])
def fill_na():
    global df
    column_name = request.form.get("col_name_fill", "")
    column_value = request.form.get("col_value_fill", "")

    if column_name == "":
        return render_template('uploaded1.html', ans_fill_na="Column name not provided")
    elif column_value == "":
        return render_template('uploaded1.html', ans_fill_na="Column value not provided")
    try:
        def is_numeric(s):
            try:
                s=float(s)
                return s
            except ValueError:
                return s
            
        column_value=is_numeric(column_value)
        df[column_name].fillna(value=column_value, inplace=True)
        df = df.dropna(subset=[column_name])
        return render_template('uploaded1.html',ans_fill_na="Filled null values")
    except KeyError:
        return render_template('uploaded1.html', ans_fill_na="Invalid column name or value ")
    

@app.route('/aboutus1')
def about_us():
    return render_template('aboutus1.html')

if __name__ == '__main__':
    app.run(debug=True)
    

import streamlit as st
import mysql.connector as sql
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


title = st.container()
dbdesc = st.container()
topProducts = st.container()
salesEmployee = st.container()
topProductLine = st.container()

with title:
    st.title('Classic Models Performance Dashboard')
    
with dbdesc:
    st.header('Database Description')
    st.caption('For this project, we used the "classicmodels" sample MySQL \
               database.  According to the creator, this database is a sample \
               of a "retailer of scale models of classic cars database. It \
               contains typical business data such as customers, products, \
               sales orders, sales order line items, etc."')
    st.caption('This database can be installed at \
               https://www.mysqltutorial.org/mysql-sample-database.aspx')

    
    
with topProducts:
    st.header('Top products in selected time period:')
    
    # Create a slider to select the range of months for evaluation
    monthrange = st.select_slider(label = 'Select range of months to evaluate',
                                  options = ['Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'],
                                  value = ['Jan', 'Dec'])
    
    # Dict to convert month string to integer
    monthmap = {'Jan': 1,
                'Feb': 2,
                'Mar': 3,
                'Apr': 4,
                'May': 5,
                'Jun': 6,
                'Jul': 7,
                'Aug': 8,
                'Sept': 9,
                'Oct': 10,
                'Nov': 11,
                'Dec': 12}

    # Select whether to order by units or dollars
    measure = st.selectbox(label = 'Order by Units or Dollars sold?',
                           options = ['Units', 'Dollars'])

    df = pd.read_csv('jbdf.csv')
    
    # Clean the data based on inputs above
    df = df[(df['ordMonth'] >= monthmap[monthrange[0]]) & (df['ordMonth'] <= monthmap[monthrange[1]])]
    df['ordRevs'] = df['quantityOrdered'] * df['priceEach']
    df = df.rename(columns = {'quantityOrdered': 'Units', 'ordRevs': 'Dollars'})
    df = df.groupby(['productCode', 'productName']).sum()[['Units', 'priceEach', 'Dollars']].reset_index().sort_values(measure, ascending = True)
    df = df.head(10).set_index('productName').drop(['productCode', 'priceEach'], axis = 1)
    
    # Create the plot using inputs above
    fig1 = plt.figure()
    plt.subplot(1,1,1)
    plt.style.use('ggplot')
    df[measure].plot.barh(legend = False)
    plt.title('Top 10 Products')
    plt.ylabel('Product Name')
    plt.xlabel('Product Sales in {0}'.format(measure))
    current_values = plt.gca().get_xticks()
    st.pyplot(fig1)
    
with salesEmployee:
    st.header('Sales under each employee at any given level: ')
    
    empJobTitles = pd.read_csv('jgjobtitles.csv')
    empJobTitles[empJobTitles['jobTitle'].str.contains('Manager')] = 'Sales Manager'
    jobTitles = pd.Series(empJobTitles['jobTitle'].unique())
    # Create a selectbox to select the position of employee
    title = st.selectbox(label = "Job title of the employee",
                      options = jobTitles.to_list())
    
    
    empNames = pd.read_csv('jgempnames.csv')
    empNames.loc[empNames[empNames['jobTitle'].str.contains('Manager')].index,'jobTitle'] = 'Sales Manager'
    empNames = empNames[empNames['jobTitle'] == title]
    
    # Create a selectbox to select the name of employee
    name = st.multiselect(label = "Choose employee(s)",
                      options = empNames['name'].to_list(),
                      default = empNames['name'].to_list())
    
    
    df1 = pd.read_csv('jgdf.csv')
    
    # Data selection
    if title == 'Sales Rep':
        df1 = df1[(df1['emp_name'].isin(name)) & (df1['jobTitle'] == title)][['emp_name', 'jobTitle', 'total_sales']]
    else:
        df1 = df1[(df1['emp_name'].isin(name)) | (df1['jobTitle'] == title)][['emp_name', 'jobTitle', 'total_sales']]
    
    
    # Create the plot using inputs above
    fig1 = plt.figure(figsize = (6,4))
    plt.subplot(1,1,1)
    plt.style.use('ggplot')
    plt.bar(df1['emp_name'], height = df1['total_sales'])
    plt.title('Sales under employee')
    plt.ylabel('Sales (in thousands)')
    plt.xlabel('Employee name')
    plt.xticks(rotation=85)
    current_values = plt.gca().get_xticks()
    st.pyplot(fig1)


import mysql.connector
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from PIL import Image
from decimal import Decimal

#######################
# Page configuration
st.set_page_config(
    page_title="AdventureWorks Sales Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# Fungsi untuk memformat angka
def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'

#######################
# Koneksi ke database
try:
    mydb = pymysql.connect(
        host="kubela.id",
        user="davis2024irwan",
        passwd="wh451n9m@ch1n3",
        port=3306,
        database="aw"
    )
except pymysql.Error as err:
    st.error(f"Error: {err}")
else:
    mycursor = mydb.cursor()

    # Query untuk mendapatkan daftar nama territory dan tahun
    query_category_product = """
    SELECT distinct pc.EnglishProductCategoryName
    from factinternetsales f 
    join dimproduct p on f.ProductKey = p.ProductKey 
    join dimproductsubcategory psc on p.ProductSubcategoryKey = psc.ProductSubcategoryKey 
    join dimproductcategory pc on psc.ProductCategoryKey = pc.ProductCategoryKey;
    """
    mycursor.execute(query_category_product)
    result_category_product = mycursor.fetchall()

    category_list = sorted(set([row[0] for row in result_category_product]))
    category_list.insert(0, 'All')  # Tambahkan opsi 'All' sebagai elemen pertama
    
    # Sidebar filters
    with st.sidebar:
        st.title('🚀 AdventureWorks Sales Dashboard')

        selected_category = st.selectbox('Select Category Product', category_list)

        if selected_category == 'All':
            query_sales = """
            SELECT 
                SUM(f.OrderQuantity) AS TotalProductSold,
                count(distinct c.CustomerKey) AS TotalCustomer,
                st.SalesTerritoryRegion AS Region,
                p.EnglishProductName AS ProductName,
                psc.EnglishProductSubcategoryName AS ProductSubCategory,
                pc.EnglishProductCategoryName AS ProductCategory,
                c.CustomerKey AS CustomerKey,
                c.Gender as Gender,
                p.ProductKey AS ProductKey
            FROM factinternetsales f
            JOIN dimproduct p ON f.ProductKey = p.ProductKey 
            JOIN dimproductsubcategory psc ON p.ProductSubcategoryKey = psc.ProductSubcategoryKey 
            JOIN dimproductcategory pc ON psc.ProductCategoryKey = pc.ProductCategoryKey
            JOIN dimsalesterritory st ON f.SalesTerritoryKey = st.SalesTerritoryKey 
            JOIN dimcustomer c on f.CustomerKey = c.CustomerKey
            GROUP BY Region, ProductName, ProductSubCategory, ProductCategory, CustomerKey, Gender, ProductKey;
            """
            query_line_chart = """
            select YEAR(t.FullDateAlternateKey) AS OrderYear, SUM(f.OrderQuantity) AS ProductSold
            from factinternetsales f 
            join dimtime t on f.OrderDateKey = t.TimeKey 
            join dimproduct p on f.ProductKey = p.ProductKey 
            join dimproductsubcategory psc on p.ProductSubcategoryKey = psc.ProductSubcategoryKey 
            join dimproductcategory pc on psc.ProductCategoryKey = pc.ProductCategoryKey 
            GROUP BY OrderYear
            ORDER BY OrderYear;
            """
            query_scatter = """
            SELECT EmployeeKey AS EmployeeID, Gender, BaseRate 
            FROM dimemployee
            ORDER BY EmployeeID;
            """
        else:
            query_sales = f"""
            SELECT 
                SUM(f.OrderQuantity) AS TotalProductSold,
                count(distinct c.CustomerKey) AS TotalCustomer,
                st.SalesTerritoryRegion AS Region,
                p.EnglishProductName AS ProductName,
                psc.EnglishProductSubcategoryName AS ProductSubCategory,
                pc.EnglishProductCategoryName AS ProductCategory,
                c.CustomerKey AS CustomerKey,
                c.Gender as Gender,
                p.ProductKey AS ProductKey
            FROM factinternetsales f
            JOIN dimproduct p ON f.ProductKey = p.ProductKey 
            JOIN dimproductsubcategory psc on p.ProductSubcategoryKey = psc.ProductSubcategoryKey 
            JOIN dimproductcategory pc ON psc.ProductCategoryKey = pc.ProductCategoryKey
            JOIN dimsalesterritory st ON f.SalesTerritoryKey = st.SalesTerritoryKey 
            JOIN dimcustomer c on f.CustomerKey = c.CustomerKey
            WHERE pc.EnglishProductCategoryName = '{selected_category}'
            GROUP BY Region, ProductName, ProductSubCategory, ProductCategory, CustomerKey, Gender, ProductKey;
            """
            query_line_chart = f"""
            select YEAR(t.FullDateAlternateKey) AS OrderYear, SUM(f.OrderQuantity) AS ProductSold
            from factinternetsales f 
            join dimtime t on f.OrderDateKey = t.TimeKey 
            join dimproduct p on f.ProductKey = p.ProductKey 
            join dimproductsubcategory psc on p.ProductSubcategoryKey = psc.ProductSubcategoryKey 
            join dimproductcategory pc on psc.ProductCategoryKey = pc.ProductCategoryKey 
            WHERE pc.EnglishProductCategoryName = '{selected_category}'
            GROUP BY OrderYear
            ORDER BY OrderYear;
            """
            query_scatter = """
            SELECT EmployeeKey AS EmployeeID, Gender, BaseRate 
            FROM dimemployee
            ORDER BY EmployeeID;
            """

        mycursor.execute(query_sales)
        myresult = mycursor.fetchall()

        mycursor.execute(query_line_chart)
        line_chart_result = mycursor.fetchall()
        
        mycursor.execute(query_scatter)
        scatter_result = mycursor.fetchall()

    
    # Tutup cursor dan koneksi
    mycursor.close()
    mydb.close()

    # Konversi hasil query ke DataFrame
    df_sales = pd.DataFrame(myresult, columns=["TotalProductSold", "TotalCustomer", "Region", "ProductName", "ProductSubCategory", "ProductCategory", "CustomerKey", "Gender", "ProductKey"])
    df_sales['TotalProductSold'] = df_sales['TotalProductSold'].astype(float)  # Convert to float for JSON serialization
    df_line_chart = pd.DataFrame(line_chart_result, columns=["OrderYear", "TotalProductSold"])
    df_scatter = pd.DataFrame(scatter_result, columns=["EmployeeID", "Gender", "BaseRate"])

#######################
# Main Panel

# Adding a header image
header_image = Image.open('header.png')  # Replace with your image path
st.image(header_image, use_column_width=True)

st.markdown("# 🚀 AdventureWorks Sales Dashboard")
st.markdown("**Welcome to the AdventureWorks Sales Dashboard!** Here you can find insights and analytics on the sales data.")

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_sales = format_number(df_sales["TotalProductSold"].sum())
    st.metric(label="Total Sales", value=total_sales)
with col2:
    unique_customers = df_sales["CustomerKey"].nunique()
    st.metric(label="Customers", value=unique_customers)
with col3:
    total_subcategories = df_sales["ProductSubCategory"].nunique()
    st.metric(label="Product Subcategories", value=total_subcategories)
with col4:
    total_regions = df_sales["Region"].nunique()
    st.metric(label="Sales Regions", value=total_regions)

st.subheader(' ')
col1, col2 = st.columns((1.5, 3), gap='medium')

with col1:
    st.subheader(f'Total Product Sold in {selected_category}', divider='orange')
    product_sold_sum = int(df_sales["TotalProductSold"].sum()) if not df_sales.empty else 0
    st.metric(label="Number of Products", value=product_sold_sum)
    
    # DataFrame Product Terlaris
    st.subheader('Top 10 Best Selling Products', divider='orange')
    if not df_sales.empty:
        top_product = df_sales.groupby("ProductName").agg({"TotalProductSold": "sum"})
        top_product = top_product.sort_values(by="TotalProductSold", ascending=False).head(10)
    
        st.dataframe(
            top_product.reset_index(),
            hide_index=True,
            width=None,
            column_config={
                "ProductName": st.column_config.TextColumn("Product Name"),
                "TotalProductSold": st.column_config.ProgressColumn(
                    "Total Product Sold",
                    format="%d",
                    min_value=0,
                    max_value=float(top_product["TotalProductSold"].max()),
                )
            }
        )
    else:
        st.write("No data available.")
    

with col2:
    # Line Chart Total Sales per Tahun
    st.subheader('Total Product Sold per Year',divider='orange')
    if not df_line_chart.empty:
        line_chart = px.line(df_line_chart, x='OrderYear', y='TotalProductSold', width=600, height=400, markers=True, range_x=[2001, 2004])
        st.plotly_chart(line_chart)

    # Pie Chart Total Customer by Region
    if not df_sales.empty:
        st.subheader('Total Customer by Region', divider='orange')
        pie_chart = px.pie(df_sales, values='TotalCustomer', names='Region')
        pie_chart.update_layout(width=600)
        st.plotly_chart(pie_chart)

    # Menampilkan histogram ProductSubCategory
    st.subheader('Distribution Product Subcategory', divider='orange')
    hist_chart = px.histogram(df_sales, x='ProductSubCategory', labels={'ProductSubCategory': 'Product Subcategory', 'count': 'Frequency'})
    hist_chart.update_layout(width=600)
    st.plotly_chart(hist_chart)

    # Scatter plot
    st.subheader('Relation between Employee\'s Gender and Rate', divider='orange')
    scatter_chart = px.scatter(df_scatter, x='EmployeeID', y='BaseRate', color='Gender')
    scatter_chart.update_layout(width=600)
    st.plotly_chart(scatter_chart)

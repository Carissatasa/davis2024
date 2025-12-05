import pymysql
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
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["username"],
        passwd=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
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
with st.expander('About this app'):
    st.success('by CARISSA RENATASARI, NPM : 21082010041')   
    st.info('The data used for this visualization are from the AdventureWorks database (dump_aw), specifically the FactInternetSales table')
    st.warning("**Filtering:** Filtering by product category on the sidebar affects the entire visualization except for the scatter plot")
    st.success("**Dari dashboard ini, dapat dilihat bahwa..**\n- Dengan filter untuk seluruh kategori produk, dashboard menampilkan informasi total sales, customers, product subcategories, sales regions, dan total product sold pada keseluruhan produk. Total penjualan sejumlah 60ribu berarti untuk semua kategori produk, terjadi transaksi sebanyak 60ribu. Customers sejumlah 18484 berarti jumlah customer yang membeli produk. \n- Total produk yang terjual berjumlah 60398 produk untuk seluruh kategori produk. Lain lagi apabila filter diatur untuk salah satu jenis kategori produk. \n- Dalam dashboard saya juga menampilkan dataframe berisi 10 produk terlaris untuk keseluruhan kategori produk. Lalu saya menampilkan grafik garis untuk menampilkan total produk terjual tiap tahunnya, mulai dari tahun 2001 dengan produk terjual sejumlah 1013 hingga tahun 2004 dengan produk terjual sejumlah lebih dari 32ribu. Artinya terdapat peningkatan jumlah produk terjual dari tahun ke tahun. \n- Terdapat grafik pie yang saya tampilkan untuk mengetahui persebaran asal region dari customer. Paling banyak terlihat pada customer dari region Australia dengan total 22.4% dari 10 region. \n- Untuk keseluruhan kategori produk, grafik histogram menampilkan distribusi produk dilihat dari sub kategorinya. Produk paling banyak tergolong dalam sub kategori Tires and Tubes dengan total lebih dari 15ribu produk. \n- Selanjutnya, grafik scatter plot ditampilkan untuk melihat hubungan antara gender dengan gaji karyawan. Dari grafik ini bisa dilihat bahwa persebaran gaji karyawan cukup merata antara laki-laki dan perempuan. Namun dapat dilihat pula bahwa karyawan dengan gaji tertinggi dimiliki oleh karyawan berjenis kelamin laki-laki. Gaji karyawan perempuan paling tinggi berkisar \$63 sedangkan karyawan laki-laki paling tinggi di angka \$125.5.")
    st.markdown("<span style='font-size:20sp; font-weight:bold;'>VISUALIZATION DESCRIPTION</span>", unsafe_allow_html=True)
    ## Line chart - Total Product Sold per Year
    st.markdown("<span style='color:green; font-weight:bold;'>Total Product Sold per Year</span>",unsafe_allow_html=True)
    st.write("- **Chart type:** Comparison - Line chart \n- **Description:** Displays how the number of products sold changes year over year. \n- **Code:**")
    st.code("SELECT YEAR(t.FullDateAlternateKey) AS OrderYear, SUM(f.OrderQuantity) AS ProductSold \nFROM factinternetsales f \nJOIN dimtime t on f.OrderDateKey = t.TimeKey \nJOIN dimproduct p on f.ProductKey = p.ProductKey \nJOIN dimproductsubcategory psc on p.ProductSubcategoryKey = psc.ProductSubcategoryKey \nJOIN dimproductcategory pc on psc.ProductCategoryKey = pc.ProductCategoryKey \nWHERE pc.EnglishProductCategoryName = '{selected_category}' \nGROUP BY YEAR(t.FullDateAlternateKey) \nORDER BY OrderYear;")
    ## Pie chart
    st.markdown("<span style='color:green; font-weight:bold;'>Total Customer by Region</span>",unsafe_allow_html=True)
    st.write("- **Chart type:** Composition - Pie chart \n- **Description:** Shows the composition of the number of customers based on the region, filtered by the selected product category. \n- **Code:**")
    st.code("SELECT count(distinct c.CustomerKey),  st.SalesTerritoryRegion , pc.EnglishProductCategoryName \nFROM factinternetsales f \nJOIN dimsalesterritory st ON f.SalesTerritoryKey = st.SalesTerritoryKey \nJOIN dimcustomer c on f.CustomerKey = c.CustomerKey \nJOIN dimproduct p on f.ProductKey = p.ProductKey \nJOIN dimproductsubcategory psc on p.ProductSubcategoryKey = psc.ProductSubcategoryKey \nJOIN dimproductcategory pc on psc.ProductCategoryKey = pc.ProductCategoryKey \nWHERE pc.EnglishProductCategoryName = '{selected_category}' \nGROUP BY st.SalesTerritoryRegion ;")
    ## Histogram
    st.markdown("<span style='color:green; font-weight:bold;'>Distribution of Products by Subcategory</span>",unsafe_allow_html=True)
    st.write("- **Chart type:** Distribution - Bar Histogram \n- **Description:** Displays the distribution of product subcategories based on the products sold in the selected product category. \n- **Code:**")
    st.code("SELECT SUM(f.OrderQuantity) AS ProductSold, psc.EnglishProductSubcategoryName, pc.EnglishProductCategoryName \nFROM factinternetsales f \nJOIN dimproduct p on f.ProductKey = p.ProductKey \nJOIN dimproductsubcategory psc on p.ProductSubcategoryKey = psc.ProductSubcategoryKey \nJOIN dimproductcategory pc on psc.ProductCategoryKey = pc.ProductCategoryKey \nWHERE pc.EnglishProductCategoryName = '{selected_category}'\nGROUP BY psc.EnglishProductSubcategoryName ;")
    ## Scatter plot
    st.markdown("<span style='color:green; font-weight:bold;'>The Relation between Employee's Gender and Rate</span>",unsafe_allow_html=True)
    st.write("- **Chart type:** Relationship - Scatter Plot \n- **Description:** Shows the correlation between employee gender and the salary received. This visualization answers whether gender affects employee salary. \n- **Code:**")
    st.code("SELECT EmployeeKey AS EmployeeID, Gender , BaseRate \nFROM dimemployee \nORDER BY EmployeeID;")
  
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
    st.subheader('Distribution of Products by Subcategory', divider='orange')
    hist_chart = px.histogram(df_sales, x='ProductSubCategory', labels={'ProductSubCategory': 'Product Subcategory', 'count': 'Frequency'})
    hist_chart.update_layout(width=600)
    st.plotly_chart(hist_chart)

    # Scatter plot
    st.subheader('The Relation between Employee\'s Gender and Rate', divider='orange')
    scatter_chart = px.scatter(df_scatter, x='EmployeeID', y='BaseRate', color='Gender')
    scatter_chart.update_layout(width=600)
    st.plotly_chart(scatter_chart)


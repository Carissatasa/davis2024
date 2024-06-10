import mysql.connector
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

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
    mydb = mysql.connector.connect(
        host="kubela.id",
        user="davis2024irwan",
        password="wh451n9m@ch1n3",  # Ganti dengan password yang benar jika diperlukan
        database="dump-dw_aw-202403050806"  # Pastikan nama database sudah benar
    )
except mysql.connector.Error as err:
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
                MONTH(t.FullDateAlternateKey) AS OrderMonth,
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
            JOIN dimtime t ON f.OrderDateKey = t.TimeKey 
            JOIN dimproduct p ON f.ProductKey = p.ProductKey 
            JOIN dimproductsubcategory psc ON p.ProductSubcategoryKey = psc.ProductSubcategoryKey 
            JOIN dimproductcategory pc ON psc.ProductCategoryKey = pc.ProductCategoryKey
            JOIN dimsalesterritory st ON f.SalesTerritoryKey = st.SalesTerritoryKey 
            JOIN dimcustomer c on f.CustomerKey = c.CustomerKey
            GROUP BY OrderMonth, Region, ProductName, ProductSubCategory, ProductCategory, CustomerKey, Gender, ProductKey
            ORDER BY OrderMonth;
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
        else:
            query_sales = f"""
            SELECT 
                YEAR(t.FullDateAlternateKey) AS OrderYear,
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
            JOIN dimtime t ON f.OrderDateKey = t.TimeKey 
            JOIN dimproduct p ON f.ProductKey = p.ProductKey 
            JOIN dimproductsubcategory psc ON p.ProductSubcategoryKey = psc.ProductSubcategoryKey 
            JOIN dimproductcategory pc ON psc.ProductCategoryKey = pc.ProductCategoryKey
            JOIN dimsalesterritory st ON f.SalesTerritoryKey = st.SalesTerritoryKey 
            JOIN dimcustomer c on f.CustomerKey = c.CustomerKey
            WHERE pc.EnglishProductCategoryName = '{selected_category}'
            GROUP BY OrderYear, Region, ProductName, ProductSubCategory, ProductCategory, CustomerKey, Gender, ProductKey
            ORDER BY OrderYear;
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

        mycursor.execute(query_sales)
        myresult = mycursor.fetchall()

        mycursor.execute(query_line_chart)
        line_chart_result = mycursor.fetchall()

    # Tutup cursor dan koneksi
    mycursor.close()
    mydb.close()

    # Konversi hasil query ke DataFrame
    df_sales = pd.DataFrame(myresult, columns=["OrderYear", "TotalProductSold", "TotalCustomer", "Region", "ProductName", "ProductSubCategory", "ProductCategory", "CustomerKey", "Gender", "ProductKey"])
    df_line_chart = pd.DataFrame(line_chart_result, columns=["OrderYear", "TotalProductSold"])


#######################
# Main Panel
col1, col2 = st.columns((1.5, 3), gap='medium')

with col1:
    st.markdown(f'#### Total Product Sold in {selected_category}')
    product_sold_sum = int(df_sales["TotalProductSold"].sum()) if not df_sales.empty else 0
    st.metric(label="Number of Products", value=product_sold_sum)
    
    # DataFrame Product Terlaris
    st.markdown('#### Top 10 Best Selling Products')
    if not df_sales.empty:
        top_product = df_sales.groupby("ProductName").agg({"TotalProductSold": "sum"})
        top_product = top_product.sort_values(by="TotalProductSold", ascending=False).head(10)
        st.write(top_product)
    else:
        st.write("No data available.")
    

with col2:
    # # Line Chart Total Sales per Bulan
    # st.markdown('#### Total Product Sold per Month')
    # if not df_line_chart.empty:
    #     line_chart = alt.Chart(df_line_chart).mark_line().encode(
    #         x=alt.X('OrderYear:O', axis=alt.Axis(title="Month", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
    #         y=alt.Y('TotalProductSold:Q', axis=alt.Axis(title="Total Product Sold", titleFontSize=18, titlePadding=15, titleFontWeight=900))
    #     ).properties(width=600
    #     ).configure_axis(
    #         labelFontSize=12,
    #         titleFontSize=12
    #     )
    #     st.altair_chart(line_chart, use_container_width=True)
        
    # Line Chart Total Sales per Bulan dengan Plotly
    st.markdown('#### Total Product Sold per Year')
    if not df_line_chart.empty:
        line_chart = px.line(df_line_chart, x='OrderYear', y='TotalProductSold', width=600, height=400, markers=True, range_x=[2001, 2004])
        st.plotly_chart(line_chart)

    # Pie Chart Total Customer by Region
    if not df_sales.empty:
        st.markdown('#### Total Customer by Region')
        pie_chart = px.pie(df_sales, values='TotalCustomer', names='Region')
        pie_chart.update_layout(width=600)
        st.plotly_chart(pie_chart)

    # Menampilkan histogram tipe kartu kredit
    st.markdown('#### ProductSubCategory Histogram')
    hist_chart = px.histogram(df_sales, x='ProductSubCategory', labels={'ProductSubCategory': 'Product Subcategory', 'count': 'Frequency'})
    hist_chart.update_layout(width=600)
    st.plotly_chart(hist_chart)

    # Scatter plot
    st.markdown('#### Relation between Customer and His Gender at Buying Products')
    scatter_chart = px.scatter(df_sales, x='CustomerKey', y='TotalProductSold', color='Gender')
    scatter_chart.update_layout(width=600)

    st.plotly_chart(scatter_chart)

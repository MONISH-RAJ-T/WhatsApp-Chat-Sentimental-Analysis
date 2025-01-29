import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    try:
        data = bytes_data.decode('utf-8')
    
        df = preprocessor.preprocess(data)

        # fetch unique users
        user_list = df['user'].unique().tolist()
        user_list.sort()
        user_list.insert(0, 'Overall')

        selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)

        if st.sidebar.button('Show Analysis'):

            # stats area
            num_messages, words, num_media_messages, links = helper.fetch_stats(selected_user, df)

            st.title('Top Statistics')
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.header('Total Messages')
                st.title(num_messages)

            with col2:
                st.header('Total Words')
                st.title(words)

            with col3:
                st.header('Media Shared')
                st.title(num_media_messages)

            with col4:
                st.header('Links Shared')
                st.title(links)

            # monthly timeline of user
            timeline = helper.monthly_timeline(selected_user, df)
            st.title('Monthly User Activity')
            fig, ax = plt.subplots()
            ax.plot(timeline['time'],timeline['message'])
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

            # daily timeline of user
            daily_timeline = helper.daily_timeline(selected_user, df)
            st.title('Daily User Activity')
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            # activity map
            st.title('Activity Map')
            col1, col2 = st.columns(2)

            with col1:
                st.header('Most Busy Day')
                busy_day = helper.week_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.header('Most Busy Month')
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            st.title('Weekly Activity Map')
            st.header('Lighter Color means User most active')
            st.header('Darker Color means User inactive')
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)



            # finding the busiest user in the group (Group level)
            if selected_user == 'Overall':
                st.title('Most Active Users')
                x, new_df = helper.most_busy_users(df)
                fig, ax = plt.subplots()

                col1, col2 = st.columns(2)

                with col1:
                    st.header('Top 5 Users')
                    ax.bar(x.index, x.values,color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                with col2:
                    st.header('Percent Of Message')
                    st.dataframe(new_df)

            # wordcloud
            st.title('Word Cloud')
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

            # most common words
            most_common_df = helper.most_common_words(selected_user, df)

            fig, ax = plt.subplots()

            ax.barh(most_common_df['words'],most_common_df['count'])
            plt.xticks(rotation = 'vertical')
            st.title('Most Common Words')
            st.pyplot(fig)

            # emoji analysis
        
            emoji_df = helper.emoji_helper(selected_user, df)
            st.title('Emoji Analysis')

            col1, col2 = st.columns(2)

            with col1:
                st.header('Top Emoji')
                st.dataframe(emoji_df)

        
            with col2:
                try:
                    st.header('Percent of Emoji')
                    fig, ax = plt.subplots()
                    ax.pie(emoji_df['count'].head(), labels = emoji_df['emoji'].head(), autopct= '%.2f', explode = [0.2,0.2,0.2,0.2,0.2], shadow = True)
                    st.pyplot(fig)
                    plt.xticks(rotation = 'vertical')
                except:
                    st.header('No Emojis')

    except:
        st.title('Upload a txt file')
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pre
import helper


st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = pre.preprocess(data)


    user_list = df['user'].unique().tolist()
    user_list.remove('grp_notif')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

#stats
    if st.sidebar.button("Show Analysis"):
        num_msg,words,media_msg,num_links=helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4=st.columns(4)


        with col1:
            st.header("Total Messages")
            st.title(num_msg)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(media_msg)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

#monthly timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

#daily timeline
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

#activity map
        st.title('Activity Map')
        col1,col2=st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busyday=helper.weekly_activity(selected_user,df)
            fig,ax=plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busyday.index,busyday.values)
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busymonth=helper.monthly_activity(selected_user,df)
            fig,ax=plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busymonth.index,busymonth.values,color='orange')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

#busiest user
        if selected_user=='Overall':
            st.title("Busy Users")
            x,new_df=helper.mostbusyusers(df)
            fig,ax=plt.subplots()
            plt.xticks(rotation='vertical')

            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index, x.values,color='red')

                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

#wordcloud
        st.title("WordCloud")
        df_wc=helper.word_cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
#most common words
        st.title("Most Common Words")
        most_common_df=helper.most_common_words(selected_user, df)
        fig,ax=plt.subplots()
        plt.xticks(rotation='vertical')
        ax.barh(most_common_df[0],most_common_df[1],color='green')
        st.pyplot(fig)

# emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)
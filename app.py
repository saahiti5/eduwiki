import streamlit as st
import random
from datetime import datetime
import plotly.express as px
import requests

# Page config
st.set_page_config(page_title="EduWiki Offline", page_icon="🎓", layout="wide")

# CSS styling
st.markdown("""
<style>
.main-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 1rem;}
.content-card { background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 3px 15px rgba(0,0,0,0.1); margin: 0.5rem 0;}
.level-badge { background: linear-gradient(45deg, #28a745, #20c997); color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem;}
.wiki-card { background: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #007bff; margin: 1rem 0;}
</style>
""", unsafe_allow_html=True)

# Topic database
TOPIC_CATEGORIES = {
    'Science': ['Physics', 'Chemistry', 'Biology', 'Mathematics', 'Computer Science', 'Astronomy', 'Geology', 'Medicine', 'Genetics', 'Ecology', 'Quantum Physics', 'Molecular Biology', 'Organic Chemistry', 'Calculus', 'Statistics'],
    'Technology': ['Artificial Intelligence', 'Machine Learning', 'Blockchain', 'Internet of Things', 'Cybersecurity', 'Cloud Computing', 'Robotics', 'Data Science', 'Web Development', 'Mobile Technology', 'Virtual Reality', 'Augmented Reality', '5G Technology', 'Quantum Computing'],
    'History': ['Ancient Civilizations', 'World Wars', 'Indian History', 'Medieval Period', 'Renaissance', 'Industrial Revolution', 'Cold War', 'Ancient Egypt', 'Roman Empire', 'Mughal Empire', 'British Raj', 'Independence Movement', 'Archaeological Discoveries'],
    'Geography': ['Continents', 'Countries', 'Rivers', 'Mountains', 'Climate Change', 'Natural Resources', 'Population Studies', 'Urban Planning', 'Ecosystems', 'Weather Patterns', 'Ocean Currents', 'Plate Tectonics', 'Biodiversity'],
    'Arts & Literature': ['Literature', 'Music', 'Painting', 'Sculpture', 'Dance', 'Theater', 'Cinema', 'Photography', 'Architecture', 'Poetry', 'Classical Music', 'Folk Arts', 'Modern Art', 'Digital Art'],
    'Languages': ['English Grammar', 'Hindi Literature', 'Sanskrit Studies', 'Tamil Poetry', 'Bengali Literature', 'Telugu Culture', 'Marathi Arts', 'Gujarati Heritage', 'Punjabi Folk', 'Urdu Poetry', 'Language Evolution', 'Linguistics'],
    'Economics': ['Microeconomics', 'Macroeconomics', 'International Trade', 'Banking', 'Stock Market', 'Cryptocurrency', 'Economic Policy', 'Development Economics', 'Behavioral Economics', 'Game Theory'],
    'Philosophy': ['Ancient Philosophy', 'Modern Philosophy', 'Ethics', 'Logic', 'Metaphysics', 'Political Philosophy', 'Eastern Philosophy', 'Western Philosophy', 'Indian Philosophy', 'Existentialism'],
    'Health & Medicine': ['Anatomy', 'Physiology', 'Nutrition', 'Mental Health', 'Public Health', 'Pharmacology', 'Surgery', 'Pediatrics', 'Cardiology', 'Neurology', 'Traditional Medicine', 'Ayurveda'],
    'Environment': ['Climate Change', 'Renewable Energy', 'Conservation', 'Pollution', 'Sustainability', 'Green Technology', 'Wildlife Protection', 'Forest Management', 'Water Resources', 'Carbon Footprint']
}

# Translations
TRANSLATIONS = {
    'en': {'explore': 'Explore', 'learn': 'Learn', 'quiz': 'Quiz', 'analytics': 'Analytics', 'search': 'Search topics...', 'level': 'Level', 'score': 'Score'},
    'hi': {'explore': 'अन्वेषण', 'learn': 'सीखें', 'quiz': 'प्रश्नोत्तरी', 'analytics': 'विश्लेषण', 'search': 'विषय खोजें...', 'level': 'स्तर', 'score': 'अंक'},
    'ta': {'explore': 'ஆராய்', 'learn': 'கற்று', 'quiz': 'வினாடி வினா', 'analytics': 'பகுப்பாய்வு', 'search': 'தலைப்புகளைத் தேடுங்கள்...', 'level': 'நிலை', 'score': 'மதிப்பெண்'},
    'bn': {'explore': 'অন্বেষণ', 'learn': 'শিখুন', 'quiz': 'কুইজ', 'analytics': 'বিশ্লেষণ', 'search': 'বিষয় খুঁজুন...', 'level': 'স্তর', 'score': 'স্কোর'},
    'te': {'explore': 'అన్వేషణ', 'learn': 'నేర్చుకో', 'quiz': 'క్విజ్', 'analytics': 'విశ్లేషణ', 'search': 'అంశాలను వెతకండి...', 'level': 'స్థాయి', 'score': 'స్కోర్'},
    'mr': {'explore': 'शोधा', 'learn': 'शिका', 'quiz': 'प्रश्नमंजुषा', 'analytics': 'विश्लेषण', 'search': 'विषय शोधा...', 'level': 'स्तर', 'score': 'गुण'},
    'gu': {'explore': 'અન્વેષણ', 'learn': 'શીખો', 'quiz': 'ક્વિઝ', 'analytics': 'વિશ્લેષણ', 'search': 'વિષયો શોધો...', 'level': 'સ્તર', 'score': 'સ્કોર'}
}

# Wikipedia API integration
def get_wikipedia_summary(topic):
    """Fetch Wikipedia summary for a topic"""
    try:
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + topic.replace(" ", "_")
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'title': data.get('title', topic),
                'summary': data.get('extract', 'No summary available'),
                'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                'image': data.get('thumbnail', {}).get('source', '') if data.get('thumbnail') else ''
            }
    except:
        pass
    return None

def generate_content(topic):
    """Generate educational content dynamically"""
    content = f"""
    {topic} is a fundamental concept that encompasses various aspects of knowledge and understanding. This field of study involves systematic investigation, analysis, and practical application of principles that have been developed through extensive research and observation.
    
    Understanding {topic} is crucial for developing comprehensive knowledge in this field. Students and professionals in related fields benefit from comprehensive understanding of core concepts, methodologies, and current trends that shape this discipline.
    
    {topic} has wide-ranging applications in modern society and continues to evolve with new discoveries. From theoretical foundations to practical implementations, this subject area demonstrates significant relevance in solving real-world problems and advancing human knowledge.
    
    Current research in {topic} focuses on innovative approaches and technological advancements. Ongoing studies continue to reveal new insights, challenge existing paradigms, and open pathways for innovation and discovery.
    
    The future of {topic} holds promising developments that will impact various sectors. Emerging technologies, changing global needs, and interdisciplinary approaches are reshaping the landscape and creating new opportunities for growth and development.
    """
    
    return {
        'title': topic,
        'description': f"Comprehensive study of {topic}",
        'content': content.strip(),
        'category': get_category(topic),
        'difficulty': random.choice(['Beginner', 'Intermediate', 'Advanced']),
        'estimated_time': f"{random.randint(10, 45)} minutes"
    }

def get_category(topic):
    for category, topics in TOPIC_CATEGORIES.items():
        if topic in topics:
            return category
    return 'General'

def search_topics(query):
    if not query:
        return []
    
    query_lower = query.lower()
    results = []
    
    for category, topics in TOPIC_CATEGORIES.items():
        for topic in topics:
            if query_lower in topic.lower():
                results.append(topic)
    
    if len(results) < 5:
        for category, topics in TOPIC_CATEGORIES.items():
            for topic in topics:
                if any(word in topic.lower() for word in query_lower.split()):
                    if topic not in results:
                        results.append(topic)
    
    return results[:20]

def generate_quiz(topic):
    """Generate quiz questions for any topic"""
    question_types = [
        f"What is the primary focus of {topic}?",
        f"Which field is most closely related to {topic}?",
        f"What are the main applications of {topic}?",
        f"How does {topic} contribute to modern society?",
        f"What skills are essential for understanding {topic}?"
    ]
    
    questions = []
    for i, q_template in enumerate(random.sample(question_types, min(3, len(question_types)))):
        if i % 2 == 0:
            options = ['Innovation and Research', 'Practical Applications', 'Theoretical Framework', 'Historical Development']
            questions.append({
                'question': q_template,
                'options': options,
                'answer': random.choice(options),
                'type': 'mcq',
                'points': 15
            })
        else:
            questions.append({
                'question': f"The study of {topic} primarily involves _____ and analysis.",
                'answer': 'research',
                'type': 'fill',
                'points': 10
            })
    
    return questions

# Initialize session state
if 'user_score' not in st.session_state:
    st.session_state.user_score = 0
if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = []
if 'quiz_scores' not in st.session_state:
    st.session_state.quiz_scores = []
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'learning_history' not in st.session_state:
    st.session_state.learning_history = []

def t(key):
    return TRANSLATIONS.get(st.session_state.language, {}).get(key, key)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎓 EduWiki Offline - Comprehensive Learning Platform</h1>
    <p>Learn Anything, Anywhere • Complete Offline Experience</p>
</div>
""", unsafe_allow_html=True)

# Language selector
col1, col2 = st.columns([4, 1])
with col2:
    languages = {'en': '🇬🇧 English', 'hi': '🇮🇳 हिंदी', 'ta': '🇮🇳 தமிழ்', 'bn': '🇮🇳 বাংলা', 'te': '🇮🇳 తెలుగు', 'mr': '🇮🇳 मराठी', 'gu': '🇮🇳 ગુજરાતી'}
    st.session_state.language = st.selectbox("Language:", list(languages.keys()), format_func=lambda x: languages[x], index=0)

# Sidebar
with st.sidebar:
    st.header(f"📊 Your Progress")
    
    level = min(20, (st.session_state.user_score // 100) + 1)
    st.markdown(f'<div class="level-badge">{t("level")} {level}</div>', unsafe_allow_html=True)
    st.progress((st.session_state.user_score % 100) / 100)
    st.metric(t("score"), st.session_state.user_score)
    
    if st.session_state.bookmarks:
        st.subheader("🔖 Bookmarks")
        for bookmark in st.session_state.bookmarks[-3:]:
            if st.button(f"⭐ {bookmark[:20]}...", key=f"bm_{bookmark}"):
                st.session_state.selected_topic = bookmark

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs([f"🔍 {t('explore')}", f"📚 {t('learn')}", f"🧠 {t('quiz')}", f"📈 {t('analytics')}"])

with tab1:
    st.header(f"🔍 {t('explore')} Topics")
    
    search_query = st.text_input(f"🔍 {t('search')}", placeholder="AI, Physics, History, Biology...")
    
    if search_query:
        results = search_topics(search_query)
        if results:
            st.success(f"Found {len(results)} topics")
            cols = st.columns(3)
            for i, topic in enumerate(results):
                with cols[i % 3]:
                    if st.button(f"📚 {topic}", key=f"search_{topic}"):
                        st.session_state.selected_topic = topic
                        st.rerun()
    
    st.subheader("📋 Browse Categories")
    for category, topics in TOPIC_CATEGORIES.items():
        with st.expander(f"📖 {category} ({len(topics)} topics)"):
            cols = st.columns(3)
            for i, topic in enumerate(topics):
                with cols[i % 3]:
                    if st.button(topic, key=f"cat_{category}_{topic}"):
                        st.session_state.selected_topic = topic
                        st.rerun()

with tab2:
    st.header(f"📚 {t('learn')}")
    
    if 'selected_topic' not in st.session_state or not st.session_state.selected_topic:
        st.info("👆 Select a topic from Explore to start learning!")
        
        st.subheader("✨ Featured Topics")
        all_topics = [topic for topics in TOPIC_CATEGORIES.values() for topic in topics]
        featured = random.sample(all_topics, min(6, len(all_topics)))
        cols = st.columns(3)
        for i, topic in enumerate(featured):
            with cols[i % 3]:
                if st.button(f"🌟 {topic}", key=f"featured_{topic}"):
                    st.session_state.selected_topic = topic
                    st.rerun()
    else:
        topic = st.session_state.selected_topic
        content = generate_content(topic)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown(f"# 📖 {content['title']}")
            st.markdown(f"**Category:** {content['category']} | **Level:** {content['difficulty']} | **Time:** {content['estimated_time']}")
            st.markdown("---")
            st.write(content['content'])
            
            # Wikipedia Integration
            st.markdown("### 🌐 Want to Learn More?")
            col_wiki1, col_wiki2 = st.columns(2)
            
            with col_wiki1:
                if st.button("📖 Get Wikipedia Summary", type="secondary"):
                    st.session_state.show_wiki = True
            
            with col_wiki2:
                wiki_url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
                st.markdown(f"[🔗 Open Wikipedia]({wiki_url})", unsafe_allow_html=True)
            
            # Show Wikipedia summary if requested
            if hasattr(st.session_state, 'show_wiki') and st.session_state.show_wiki:
                with st.spinner("Fetching Wikipedia content..."):
                    wiki_data = get_wikipedia_summary(topic)
                    if wiki_data:
                        st.markdown('<div class="wiki-card">', unsafe_allow_html=True)
                        st.markdown(f"**📝 Wikipedia Summary: {wiki_data['title']}**")
                        if wiki_data['image']:
                            st.image(wiki_data['image'], width=200)
                        st.write(wiki_data['summary'])
                        if wiki_data['url']:
                            st.markdown(f"[📖 Read full article on Wikipedia]({wiki_data['url']})")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        if st.button("❌ Hide Wikipedia Summary"):
                            st.session_state.show_wiki = False
                            st.rerun()
                    else:
                        st.warning("Could not fetch Wikipedia content. Please check your internet connection or try the direct link.")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.info(f"📊 **Topic Info**\n- Category: {content['category']}\n- Level: {content['difficulty']}\n- Study Time: {content['estimated_time']}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🔖 Save"):
                    if topic not in st.session_state.bookmarks:
                        st.session_state.bookmarks.append(topic)
                        st.success("Saved!")
            
            with col_b:
                if st.button("✅ Done", type="primary"):
                    points = 30 + (level * 5)
                    st.session_state.user_score += points
                    st.session_state.learning_history.append({'topic': topic, 'date': datetime.now(), 'points': points})
                    st.balloons()
                    st.success(f"🎉 +{points} points!")

with tab3:
    st.header(f"🧠 {t('quiz')}")
    
    if 'selected_topic' not in st.session_state or not st.session_state.selected_topic:
        st.info("Select a topic to take a quiz!")
        
        st.subheader("🎯 Quick Quiz")
        all_topics = [topic for topics in TOPIC_CATEGORIES.values() for topic in topics]
        if st.button("🎲 Random Topic Quiz"):
            random_topic = random.choice(all_topics)
            st.session_state.selected_topic = random_topic
            st.session_state.current_quiz = generate_quiz(random_topic)
            st.rerun()
    else:
        topic = st.session_state.selected_topic
        st.subheader(f"Quiz: {topic}")
        
        if st.button("🎯 Start Quiz", type="primary"):
            st.session_state.current_quiz = generate_quiz(topic)
            st.session_state.quiz_answers = {}
            st.rerun()
        
        if 'current_quiz' in st.session_state and st.session_state.current_quiz:
            questions = st.session_state.current_quiz
            
            for i, q in enumerate(questions, 1):
                st.markdown(f"**Question {i}** ({q['points']} points)")
                st.write(q['question'])
                
                if q['type'] == 'fill':
                    answer = st.text_input("Your answer:", key=f"q_{i}")
                else:
                    choice = st.radio("Choose:", q['options'], key=f"q_{i}")
            
            if st.button("📝 Submit Quiz", type="primary"):
                score = 0
                total = sum(q['points'] for q in questions)
                
                for i, q in enumerate(questions, 1):
                    user_answer = st.session_state.get(f"q_{i}", "")
                    if q['type'] == 'fill':
                        if user_answer.lower().strip() == q['answer'].lower():
                            score += q['points']
                    else:
                        if user_answer == q['answer']:
                            score += q['points']
                
                percentage = (score / total) * 100 if total > 0 else 0
                st.session_state.user_score += score
                st.session_state.quiz_scores.append({
                    'topic': topic, 'score': percentage, 'points': score,
                    'date': datetime.now().strftime("%Y-%m-%d")
                })
                
                if percentage >= 80:
                    st.balloons()
                    st.success(f"🌟 Excellent! {score}/{total} ({percentage:.0f}%)")
                elif percentage >= 60:
                    st.success(f"👍 Good! {score}/{total} ({percentage:.0f}%)")
                else:
                    st.warning(f"📚 Keep practicing! {score}/{total} ({percentage:.0f}%)")
                
                del st.session_state.current_quiz

with tab4:
    st.header(f"📈 {t('analytics')}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Score", st.session_state.user_score)
    with col2:
        st.metric("Topics Studied", len(st.session_state.learning_history))
    with col3:
        st.metric("Quizzes Taken", len(st.session_state.quiz_scores))
    with col4:
        st.metric("Bookmarks", len(st.session_state.bookmarks))
    
    if st.session_state.quiz_scores:
        dates = [q['date'] for q in st.session_state.quiz_scores]
        scores = [q['score'] for q in st.session_state.quiz_scores]
        fig = px.line(x=dates, y=scores, title="Quiz Performance Over Time", markers=True)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("📋 Recent Activity")
        for quiz in st.session_state.quiz_scores[-5:]:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"📖 {quiz['topic']}")
            with col2:
                st.write(f"🎯 {quiz['score']:.0f}%")
            with col3:
                st.write(f"📅 {quiz['date']}")
    else:
        st.info("🚀 Start learning and taking quizzes to see your analytics!")

# Footer
st.markdown("---")
total_topics = sum(len(topics) for topics in TOPIC_CATEGORIES.values())
st.markdown(f"""
<div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; border-radius: 10px;'>
    <h4>🌟 EduWiki Offline - Complete Learning Platform</h4>
    <p><em>{total_topics}+ Topics • 7 Indian Languages • Wikipedia Integration • Full Offline Experience</em></p>
</div>
""", unsafe_allow_html=True)

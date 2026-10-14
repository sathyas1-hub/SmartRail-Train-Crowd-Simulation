import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(page_title='SmartRail | Train & Crowd Simulator', page_icon='🚆', layout='wide')
st.markdown('''<style>.block-container{padding-top:1.2rem}.hero{padding:1.4rem;border-radius:18px;background:linear-gradient(120deg,#102746,#176B87);color:white;margin-bottom:1rem}.hero h1{color:white;margin:0}.hero p{color:#dceef4;margin:.45rem 0 0}.coach{border:1px solid #dce5eb;border-radius:14px;padding:1rem;background:white;min-height:140px}.small{color:#617482;font-size:.82rem}</style>''', unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>🚆 SmartRail — Local Train Simulation</h1><p>Train movement • Compartment-wise crowd levels • Passenger-friendly coach recommendation</p></div>', unsafe_allow_html=True)
st.warning('SIMULATION MODE: train movement, ETA and crowd values are generated demo data. This app is not connected to Indian Railways or live sensors.')
with st.sidebar:
    st.header('⚙️ Simulation Controls')
    train = st.selectbox('Train', ['Local Train 206','Local Train 208','Local Train 210'])
    start = st.selectbox('Starting station',['Madurai Junction','Koodal Nagar','Tirupparankundram'])
    nxt = st.selectbox('Next station',['Madurai Junction','Koodal Nagar','Tirupparankundram','Thirumangalam'])
    duration = st.slider('Journey duration (demo minutes)',10,60,40,5)
    progress = st.slider('Simulated journey progress',0,100,58,1)
    st.divider(); st.subheader('Crowd scenario')
    capacity = st.number_input('Illustrative capacity per coach',20,250,100,10)
    counts = [st.slider(f'Coach C{i} passengers',0,int(capacity*1.5),v) for i,v in enumerate([35,92,68,42],1)]
    if st.button('🎲 Generate new demo crowd',use_container_width=True):
        st.session_state.counts = np.random.default_rng().integers(10,max(20,int(capacity*1.3)),4).tolist()
    if 'counts' in st.session_state: counts = st.session_state.counts

coaches=['C1','C2','C3','C4']; perc=[round(n/capacity*100) for n in counts]
def level(p): return ('LOW','#198754') if p<=50 else (('MEDIUM','#d89b00') if p<=80 else ('HIGH','#cf3f49'))
levels=[level(p)[0] for p in perc]; eta=max(1,round((100-progress)/100*duration)); best=coaches[int(np.argmin(perc))]
k1,k2,k3,k4=st.columns(4)
k1.metric('Train',train); k2.metric('Journey progress',f'{progress}%'); k3.metric('Demo ETA',f'{eta} min'); k4.metric('High-crowd coaches',sum(x=='HIGH' for x in levels))
t1,t2,t3=st.tabs(['🗺️ Train Tracking','👥 Coach Crowd','🧪 Test Scenarios'])
with t1:
    a,b=st.columns([1.2,1])
    with a:
        st.subheader('Illustrative route progress')
        route=[start,'Route checkpoint A','Route checkpoint B',nxt]
        fig=go.Figure(); fig.add_trace(go.Scatter(x=[0,1,2,3],y=[0]*4,mode='lines',line=dict(width=8,color='#c8d7e2'),showlegend=False,hoverinfo='skip'))
        fig.add_trace(go.Scatter(x=[0,1,2,3],y=[0]*4,mode='markers+text',marker=dict(size=22,color=['#176B87','#176B87','#176B87','#dfe8ee']),text=route,textposition='bottom center',showlegend=False))
        fig.add_trace(go.Scatter(x=[progress/100*3],y=[0],mode='markers',marker=dict(size=28,color='#f0b43c',line=dict(width=3,color='white')),name='Demo train'))
        fig.update_layout(height=270,margin=dict(l=10,r=10,t=15,b=70),xaxis=dict(visible=False,range=[-.3,3.3]),yaxis=dict(visible=False,range=[-.8,.8]),plot_bgcolor='white',paper_bgcolor='white')
        st.plotly_chart(fig,use_container_width=True); st.caption('Visual route only; not a real railway map or GPS fix.')
    with b:
        st.subheader('Train status'); st.write(f'**Selected train:** {train}'); st.write(f'**From:** {start}'); st.write(f'**Next station:** {nxt}'); st.write(f'**Estimated arrival:** {eta} simulated minutes'); st.progress(progress/100)
        st.info('Demo ETA is calculated from sliders, not from a railway timetable.')
with t2:
    st.subheader('Compartment-wise crowd monitoring'); st.caption('Occupancy = demo passenger count ÷ illustrative capacity. Values may exceed 100%.')
    cols=st.columns(4)
    for i,col in enumerate(cols):
        label,color=level(perc[i])
        with col:
            st.markdown(f'<div class="coach"><div class="small">COMPARTMENT</div><div style="font-size:1.7rem;font-weight:800;color:#15334a">{coaches[i]}</div><div style="font-size:1.35rem;font-weight:750;color:{color}">{label}</div><div>{perc[i]}% occupied</div><div class="small">{counts[i]} demo passengers / {capacity} capacity</div></div>',unsafe_allow_html=True)
            st.progress(min(perc[i],100)/100)
    df=pd.DataFrame({'Compartment':coaches,'Demo passengers':counts,'Illustrative capacity':[capacity]*4,'Occupancy (%)':perc,'Crowd level':levels})
    fig=go.Figure(go.Bar(x=coaches,y=perc,marker_color=[level(p)[1] for p in perc],text=[f'{p}%' for p in perc],textposition='outside'))
    fig.add_hline(y=50,line_dash='dot',line_color='#198754'); fig.add_hline(y=80,line_dash='dot',line_color='#d89b00')
    fig.update_layout(height=320,yaxis_title='Illustrative occupancy (%)',yaxis_range=[0,max(120,max(perc)+20)],plot_bgcolor='white',paper_bgcolor='white')
    st.plotly_chart(fig,use_container_width=True); st.success(f'Demo recommendation: consider {best}, which has the lowest displayed occupancy ({min(perc)}%).')
    st.download_button('⬇️ Download crowd table (CSV)',df.to_csv(index=False).encode(), 'smarttrain_demo_crowd.csv','text/csv')
with t3:
    scenario=st.selectbox('Choose a scenario',['Normal weekday','Peak-hour rush','Festival crowd','Balanced crowd distribution'])
    scenarios={'Normal weekday':[35,48,42,30],'Peak-hour rush':[92,115,86,72],'Festival crowd':[120,135,98,110],'Balanced crowd distribution':[55,58,52,57]}
    vals=scenarios[scenario]; ps=[round(v/capacity*100) for v in vals]
    sdf=pd.DataFrame({'Compartment':coaches,'Demo passengers':vals,'Occupancy (%)':ps,'Crowd level':[level(p)[0] for p in ps]})
    st.dataframe(sdf,use_container_width=True,hide_index=True); st.info(f'Scenario recommendation: {coaches[int(np.argmin(ps))]}. Preset demo data only.')
st.divider(); st.subheader('System architecture (prototype plan)')
cols=st.columns(4)
cols[0].markdown('### 📍 GPS module\nPlanned input: coordinates after valid GPS fix.')
cols[1].markdown('### 📷 Camera / sensor\nNeeds testing and validated crowd estimation.')
cols[2].markdown('### 🧠 Processing\nClassifies occupancy into Low / Medium / High.')
cols[3].markdown('### 📱 Dashboard\nShows route progress, coach levels and recommendation.')
with st.expander('What is simulated and what is not?'):
    st.markdown('**Simulated:** train progress, demo ETA, route checkpoints, coach passenger counts, crowd classification and recommendation.\n\n**Not connected:** Indian Railways live feed, NEO-6M GPS serial data, ESP32-CAM stream, automated passenger counting or official platform notifications.')
st.caption('SmartRail student prototype • For demonstration and design review only • Not an official railway service')

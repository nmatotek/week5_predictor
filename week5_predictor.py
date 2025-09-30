import streamlit as st
import pandas as pd

# --- Load Data ---
offense_df = pd.read_csv("cleaned_offense.csv")
defense_df = pd.read_csv("cleaned_defense.csv")

teams_df = pd.merge(offense_df, defense_df, on="Team")
team_names = teams_df["Team"].tolist()

# --- Team Logos ---
team_logos = {
    "49ers": "https://a.espncdn.com/i/teamlogos/nfl/500/sf.png",
    "Bears": "https://a.espncdn.com/i/teamlogos/nfl/500/chi.png",
    "Bengals": "https://a.espncdn.com/i/teamlogos/nfl/500/cin.png",
    "Bills": "https://a.espncdn.com/i/teamlogos/nfl/500/buf.png",
    "Broncos": "https://a.espncdn.com/i/teamlogos/nfl/500/den.png",
    "Browns": "https://a.espncdn.com/i/teamlogos/nfl/500/cle.png",
    "Buccaneers": "https://a.espncdn.com/i/teamlogos/nfl/500/tb.png",
    "Cardinals": "https://a.espncdn.com/i/teamlogos/nfl/500/ari.png",
    "Chargers": "https://a.espncdn.com/i/teamlogos/nfl/500/lac.png",
    "Chiefs": "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png",
    "Colts": "https://a.espncdn.com/i/teamlogos/nfl/500/ind.png",
    "Commanders": "https://a.espncdn.com/i/teamlogos/nfl/500/wsh.png",
    "Cowboys": "https://a.espncdn.com/i/teamlogos/nfl/500/dal.png",
    "Dolphins": "https://a.espncdn.com/i/teamlogos/nfl/500/mia.png",
    "Eagles": "https://a.espncdn.com/i/teamlogos/nfl/500/phi.png",
    "Falcons": "https://a.espncdn.com/i/teamlogos/nfl/500/atl.png",
    "Giants": "https://a.espncdn.com/i/teamlogos/nfl/500/nyg.png",
    "Jaguars": "https://a.espncdn.com/i/teamlogos/nfl/500/jax.png",
    "Jets": "https://a.espncdn.com/i/teamlogos/nfl/500/nyj.png",
    "Lions": "https://a.espncdn.com/i/teamlogos/nfl/500/det.png",
    "Packers": "https://a.espncdn.com/i/teamlogos/nfl/500/gb.png",
    "Panthers": "https://a.espncdn.com/i/teamlogos/nfl/500/car.png",
    "Patriots": "https://a.espncdn.com/i/teamlogos/nfl/500/ne.png",
    "Raiders": "https://a.espncdn.com/i/teamlogos/nfl/500/lv.png",
    "Rams": "https://a.espncdn.com/i/teamlogos/nfl/500/lar.png",
    "Ravens": "https://a.espncdn.com/i/teamlogos/nfl/500/bal.png",
    "Saints": "https://a.espncdn.com/i/teamlogos/nfl/500/no.png",
    "Seahawks": "https://a.espncdn.com/i/teamlogos/nfl/500/sea.png",
    "Steelers": "https://a.espncdn.com/i/teamlogos/nfl/500/pit.png",
    "Texans": "https://a.espncdn.com/i/teamlogos/nfl/500/hou.png",
    "Titans": "https://a.espncdn.com/i/teamlogos/nfl/500/ten.png",
    "Vikings": "https://a.espncdn.com/i/teamlogos/nfl/500/min.png",
}

# --- Helper Functions ---
def calculate_expected_offense(row):
    # A = Rushing Yards per Game
    # B = Passing Yards per Game
    # C = Giveaways per Game
    # D = Red Zone TD %
    # E = FG%
    A = row['Rushing Yards per Game']
    B = row['Passing Yards per Game']
    C = row['Giveaways per Game']
    D = row['Red Zone TD %']
    E = row['FG%']
    return 0.09*A + 0.09*B - 2.88*C + 10.27*D + 7.25*E - 16.31

def calculate_expected_defense(row):
    # F = Defensive Rushing Yards per Game
    # G = Defensive Passing Yards per Game
    # H = Takeaways per Game
    # I = Defensive Red Zone TD %
    F = row['Defensive Rushing Yards per Game']
    G = row['Defensive Passing Yards per Game']
    H = row['Takeaways per Game']
    I = row['Defensive Red Zone TD %']
    return 0.07*F + 0.003*G - 2.20*H + 21.87*I + 3.80

def predict_score(team1, team2):
    t1 = teams_df[teams_df['Team'] == team1].iloc[0]
    t2 = teams_df[teams_df['Team'] == team2].iloc[0]

    t1_off = calculate_expected_offense(t1)
    t1_def = calculate_expected_defense(t1)

    t2_off = calculate_expected_offense(t2)
    t2_def = calculate_expected_defense(t2)

    team1_score = round((t1_off + t2_def) / 2, 1)
    team2_score = round((t2_off + t1_def) / 2, 1)

    return team1_score, team2_score

# --- Streamlit UI ---
st.set_page_config(page_title="NFL Week 5 Predictor", layout="wide")
st.title("🏈 NFL Week 5 Matchup Predictor")

st.markdown("Pick two teams below to simulate a matchup based on statistical scoring models.")

col1, col2 = st.columns(2)

with col1:
    team1 = st.selectbox("Select Team 1", team_names, index=0)

with col2:
    team2 = st.selectbox("Select Team 2", team_names, index=1)

if team1 == team2:
    st.warning("Please select two different teams.")
else:
    score1, score2 = predict_score(team1, team2)

    st.markdown("---")
    st.subheader("📊 Matchup Summary")

    col1, col2, col3 = st.columns([4, 1, 4])

    with col1:
        if team1 in team_logos:
            st.image(team_logos[team1], width=100)
        st.metric(label=f"{team1} Score", value=score1)
    with col2:
        st.markdown("<h3 style='text-align: center;'>VS</h3>", unsafe_allow_html=True)
    with col3:
        if team2 in team_logos:
            st.image(team_logos[team2], width=100)
        st.metric(label=f"{team2} Score", value=score2)

    with st.expander("🧮 Calculation Breakdown"):
        t1 = teams_df[teams_df['Team'] == team1].iloc[0]
        t2 = teams_df[teams_df['Team'] == team2].iloc[0]

        # Team 1 variables
        A1 = t1['Rushing Yards per Game']
        B1 = t1['Passing Yards per Game']
        C1 = t1['Giveaways per Game']
        D1 = t1['Red Zone TD %']
        E1 = t1['FG%']
        F1 = t1['Defensive Rushing Yards per Game']
        G1 = t1['Defensive Passing Yards per Game']
        H1 = t1['Takeaways per Game']
        I1 = t1['Defensive Red Zone TD %']

        # Team 2 variables
        A2 = t2['Rushing Yards per Game']
        B2 = t2['Passing Yards per Game']
        C2 = t2['Giveaways per Game']
        D2 = t2['Red Zone TD %']
        E2 = t2['FG%']
        F2 = t2['Defensive Rushing Yards per Game']
        G2 = t2['Defensive Passing Yards per Game']
        H2 = t2['Takeaways per Game']
        I2 = t2['Defensive Red Zone TD %']

        # Calculate expected offense and defense for both teams
        t1_off = 0.09*A1 + 0.09*B1 - 2.88*C1 + 10.27*D1 + 7.25*E1 - 16.31
        t1_def = 0.07*F1 + 0.003*G1 - 2.20*H1 + 21.87*I1 + 3.80
        t2_off = 0.09*A2 + 0.09*B2 - 2.88*C2 + 10.27*D2 + 7.25*E2 - 16.31
        t2_def = 0.07*F2 + 0.003*G2 - 2.20*H2 + 21.87*I2 + 3.80

        st.markdown(f"### {team1} Calculations")
        st.code(f"""
Offensive Expected Points:
0.09*A + 0.09*B - 2.88*C + 10.27*D + 7.25*E - 16.31

Substituted:
0.09*{A1:.2f} + 0.09*{B1:.2f} - 2.88*{C1:.2f} + 10.27*{D1:.2f} + 7.25*{E1:.2f} - 16.31
= {t1_off:.2f}

Defensive Expected Points Against:
0.07*F + 0.003*G - 2.20*H + 21.87*I + 3.80

Substituted:
0.07*{F1:.2f} + 0.003*{G1:.2f} - 2.20*{H1:.2f} + 21.87*{I1:.2f} + 3.80
= {t1_def:.2f}

Predicted Score:
({t1_off:.2f} + {t2_def:.2f}) / 2 = {(t1_off + t2_def) / 2:.2f}
""")

        st.markdown(f"### {team2} Calculations")
        st.code(f"""
Offensive Expected Points:
0.09*A + 0.09*B - 2.88*C + 10.27*D + 7.25*E - 16.31

Substituted:
0.09*{A2:.2f} + 0.09*{B2:.2f} - 2.88*{C2:.2f} + 10.27*{D2:.2f} + 7.25*{E2:.2f} - 16.31
= {t2_off:.2f}

Defensive Expected Points Against:
0.07*F + 0.003*G - 2.20*H + 21.87*I + 3.80

Substituted:
0.07*{F2:.2f} + 0.003*{G2:.2f} - 2.20*{H2:.2f} + 21.87*{I2:.2f} + 3.80
= {t2_def:.2f}

Predicted Score:
({t2_off:.2f} + {t1_def:.2f}) / 2 = {(t2_off + t1_def) / 2:.2f}
""")

    st.markdown("---")
    st.subheader("📈 Raw Data")
    st.markdown("### Team Statistics Breakdown")
    stat_col1, stat_col2 = st.columns(2)

    # Define columns with positive and negative impacts for styling
    positive_impact_cols = ['Red Zone TD %', 'FG%', 'Takeaways per Game']
    negative_impact_cols = ['Giveaways per Game', 'Defensive Red Zone TD %', 'Defensive Rushing Yards per Game', 'Defensive Passing Yards per Game']

    def style_stats(df):
        def highlight_cells(val, col):
            if col in positive_impact_cols:
                color = 'lightgreen' if val > 0 else ''
            elif col in negative_impact_cols:
                color = 'salmon' if val > 0 else ''
            else:
                color = ''
            return f'background-color: {color}'
        styled = df.style.apply(lambda x: [highlight_cells(v, x.name) for v in x], axis=0)
        return styled

    with stat_col1:
        st.write(f"**{team1} Stats:**")
        df1 = teams_df[teams_df['Team'] == team1].copy().T
        df1.columns = [team1]
        st.dataframe(style_stats(df1), use_container_width=True)
    with stat_col2:
        st.write(f"**{team2} Stats:**")
        df2 = teams_df[teams_df['Team'] == team2].copy().T
        df2.columns = [team2]
        st.dataframe(style_stats(df2), use_container_width=True)

    st.markdown("---")
    st.subheader("📅 Week 5 Full Matchups")

    week5_matchups = [
        ("Bears", "Commanders"),
        ("Jaguars", "Bills"),
        ("Texans", "Falcons"),
        ("Panthers", "Lions"),
        ("Titans", "Colts"),
        ("Giants", "Dolphins"),
        ("Saints", "Patriots"),
        ("Ravens", "Steelers"),
        ("Eagles", "Rams"),
        ("Bengals", "Cardinals"),
        ("Jets", "Broncos"),
        ("Chiefs", "Vikings"),
        ("Cowboys", "49ers"),
        ("Packers", "Raiders")
    ]

    # Collect predictions for export
    predictions_list = []

    for t1, t2 in week5_matchups:
        if t1 not in team_names or t2 not in team_names:
            continue
        s1, s2 = predict_score(t1, t2)
        predictions_list.append({"Team 1": t1, "Team 2": t2, "Team 1 Score": s1, "Team 2 Score": s2})
        cols = st.columns([4, 1, 4])
        with cols[0]:
            if t1 in team_logos:
                st.image(team_logos[t1], width=60)
            st.metric(label=t1, value=s1)
        with cols[1]:
            st.markdown("<h4 style='text-align: center;'>VS</h4>", unsafe_allow_html=True)
        with cols[2]:
            if t2 in team_logos:
                st.image(team_logos[t2], width=60)
            st.metric(label=t2, value=s2)

    st.markdown("---")
    st.subheader("📤 Export")
    predictions_df = pd.DataFrame(predictions_list)
    csv_data = predictions_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download as CSV",
        data=csv_data,
        file_name='week5_predictions.csv',
        mime='text/csv'
    )
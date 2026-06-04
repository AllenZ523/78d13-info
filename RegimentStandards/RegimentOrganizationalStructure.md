::: mermaid
flowchart BT
    %% 新人（最底部）
    Newbie[("新人 [N]")]

    %% 普通队员
    Ordinary[("普通队员")]

    %% 常驻领队
    Captain[("常驻领队 [C]")]

    %% 教学组、比赛组
    TeachingGroup[("教学组")]
    MatchGroup[("比赛组")]

    %% 决策组、队长
    DecisionGroup[("决策组")]
    Leader[("队长 / 副队长")]

    %% 晋升路径（自下而上）
    Newbie -->|萌新课培养| Ordinary
    Ordinary -->|截图+实操考核| Captain

    %% 常驻领队可自愿参与比赛组
    Captain -->|自愿参与| MatchGroup

    %% 教学组来源：比赛组考核产生
    MatchGroup -->|笔试+实操+截图| TeachingGroup

    %% 教学组职责：培养新人、进阶课、输送人才
    TeachingGroup -->|开设萌新课| Newbie
    TeachingGroup -->|开设进阶课| Captain
    TeachingGroup -->|输送人才| MatchGroup

    %% 顶层管理关系
    Leader -->|直接管理| TeachingGroup
    Leader -->|直接管理| MatchGroup
    Leader -->|直接管理| Captain

    %% 决策组产生方式
    Leader -->|选拔+推荐| DecisionGroup
    Captain -->|选拔+推荐| DecisionGroup
    Ordinary -->|选拔+推荐| DecisionGroup

    %% 决策组对队长的制衡
    DecisionGroup -->|70%反对可否决| Leader

    %% 样式
    classDef bottom fill:#ffc,stroke:#333
    classDef middle fill:#dfd,stroke:#333
    classDef top fill:#f9f,stroke:#333,stroke-width:2px
    classDef decision fill:#bbf,stroke:#333
    class Newbie bottom
    class Ordinary,Captain middle
    class TeachingGroup,MatchGroup top
    class DecisionGroup decision
    class Leader top
:::
{
    "outbound": [
        {
            "match": 
            {
                "tcp_dst": 80
            },
            "action": 
            {
                "fwd": 2
            }
        },
        {
            "match": 
            {
                "tcp_dst": 443
            },
            "action": 
            {
                "fwd": 3
            }
        }
    ]
}

{
    "inbound": [
        {
            "match": 
            {
                "tcp_dst": 443
            },
            "action": 
            {
                "fwd": 0
            }
        },
        {
            "match": 
            {
                "tcp_dst": 80
            },
            "action": 
            {
                "fwd": 1
            }
        }
    ]
}

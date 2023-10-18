from os import system

def host_conn_setup(o_socket):
    mode_chosen = False
    c_mode = ""

    while not mode_chosen:
        c_mode = input("Host (h) or Join (j) game: ").strip().lower()
        if c_mode == "h":
            mode_chosen = True
        elif c_mode == "j":
            mode_chosen = True

    if c_mode == "h":
        print("===========================================")
        print("Host Mode")
        print("===========================================")
        own_port = int(input("Run game at port: "))
        o_socket.bind(("", own_port))
        print("===========================================")
        print(f"Game ist hosted on Port:{own_port}")
        print("===========================================")

        while True:
            rec_data, rec_f_addr = o_socket.recvfrom(1024)
            if rec_data.decode("utf-8") == "PySchiffeVersenkenByNicoConnReq":
                break
        o_socket.sendto("PySchiffeVersenkenByNicoConnAcc".encode("utf-8"), rec_f_addr)
        print("Connected to client!")

        return c_mode, rec_f_addr

    elif c_mode == "j":
        print("===========================================")
        print("Join Host")
        print("===========================================")
        own_port = int(input("Run game at port: "))
        o_socket.bind(("", own_port))
        print("===========================================")
        conn_addr = input("Host IP: ").strip()
        conn_port = int(input("Host port: "))
        print("===========================================")

        o_socket.sendto("PySchiffeVersenkenByNicoConnReq".encode("utf-8"), (conn_addr, conn_port))

        while True:
            rec_data, rec_f_addr = o_socket.recvfrom(1024)
            if rec_data.decode("utf-8") == "PySchiffeVersenkenByNicoConnAcc":
                break
        print("Connected to host!")

        return c_mode, rec_f_addr

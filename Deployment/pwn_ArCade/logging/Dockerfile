FROM ubuntu:20.04

# Invariants
ARG PORT=4567
ARG USERNAME=user
ENV USERNAME ${USERNAME}
RUN useradd -m $USERNAME
RUN apt-get update && apt-get install -y \
    xinetd \
    && rm -rf /var/lib/apt/lists/*

# Challenge files
ADD chal /home/$USERNAME/
ADD scoreboard /home/$USERNAME/scoreboard

RUN chmod -R 555 /home/$USERNAME && \
    chmod 111 /home/$USERNAME/get_flag && \
    chmod 777 /home/$USERNAME/scoreboard
ADD xinetd.conf /etc/xinetd.d/chal
EXPOSE $PORT

CMD [ \
        "xinetd", \
        "-dontfork", \
        "-f", "/etc/xinetd.d/chal" \
    ]

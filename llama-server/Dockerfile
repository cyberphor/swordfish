FROM alpine:3.22 AS build
WORKDIR /home/narwhal
ENV GGML_NATIVE=ON
ENV GGML_CPU_ARM_ARCH=""
RUN apk add --no-cache cmake curl-dev git g++ make linux-headers &&\
    git clone --depth 1 https://github.com/ggml-org/llama.cpp . &&\
    cmake -B build -DGGML_NATIVE=ON -DGGML_CPU_ARM_ARCH="" -DLLAMA_BUILD_SERVER=ON -DLLAMA_CURL=ON -DLLAMA_JINJA=ON -DBUILD_SHARED_LIBS=OFF &&\
    cmake --build build --target llama-server --config Release &&\
    cp build/bin/llama-server /home/narwhal/

FROM alpine:3.22
WORKDIR /home/narwhal
COPY --from=build /home/narwhal/llama-server .
COPY gemma-3-1b-pt-q4_0.gguf gemma-3-1b-pt-q4_0.gguf
COPY entrypoint.sh entrypoint.sh
RUN apk add --no-cache libcurl libgomp libstdc++ &&\
    chmod +x llama-server &&\
    chmod +x entrypoint.sh
EXPOSE 8080
CMD [ "./entrypoint.sh" ]

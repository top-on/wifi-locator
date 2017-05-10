FROM python:3.6-alpine

RUN apk --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/v3.5/community add \
    lapack libstdc++ \
  && apk --no-cache add --virtual .build-deps \
    build-base gfortran subversion \
  && apk --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/v3.5/community add --virtual .build-deps \
    lapack-dev \
  && ln -s /usr/include/locale.h /usr/include/xlocale.h \
  && pip install \
    "pandas~=0.20.1" \
    "scipy~=0.19.0" \
    "sklearn-pandas~=1.3.0" \
  && apk del .build-deps

    # "numpy~=1.12.1" \

WORKDIR /usr/src/app
COPY ./src /usr/src/app

# CMD [""]

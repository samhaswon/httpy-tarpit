# httpy-tarpit

An HTTP tarpit written in Python. 

It sends the start of an HTML file (in case bots look for that) followed by as much junk as the bot will consume.
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <script type="text/javascript">
        window.location="data:text/html;base64,
```

It also masquerades as a variety of servers, because that might be useful. 

## Supported Architectures
| Architecture | Available | Tag    |
|:------------:|:---------:|--------|
|    x86-64    |     ✅     | latest |
|   arm64v8    |     ✅     | latest |
|   arm32v7    |     ✅     | latest |
|   arm32v6    |     ✅     | latest |
|     i386     |     ✅     | latest |

## Setup

You have the choice of the following modes:

- `mist` mist a byte every 5 to 10 seconds. 
- `drip` drips 128 B response chunks every second.
- `trickle` trickles 1 kiB response chunks every half-second.
- `flood` sends 1024 kiB response chunks as fast as possible, but with a 0.1ms delay for accepting other connections. 
- `random` randomly chooses from the above options.

### Docker run
```shell
docker run -dp 8080:8080 \
       --restart=unless-stopped \
       --name httpy-tarpit \
       -e MODE=random \
       samhaswon/httpy-tarpit
```

### Docker Compose
```yml
services:
  httpy-tarpit:
    image: samhaswon/httpy-tarpit
    container_name: httpy-tarpit
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - TZ=America/New_York  # your linux timezone
      - MODE=random
```

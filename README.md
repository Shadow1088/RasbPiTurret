
(Important stuff are **bold**)

## History and my goal

Purpose of this repository and project was to code and create **a vision-based self-controlling turret** (Sentry). As mentioned it uses camera for vision. The second prototype of such turret has been made from cardboard, crafted by precision and final goal in mind. The turret was made of base, containing a **raspberyy pi** and a battery pack providing exterenal power source to the servo motors MG995 that ensured movement by X and Y axis. There was a lot of space for powerbank too, making my turret seemingly more portable. Then there were two pillars supporting the final part - the head. In the head was located laser and a camera, the head had a hole for each. At first it could seem just like eyes.
I found a **recognition model YOLOv5 on PyTorch**, which was convenient, as a few lines of code were enough for the human recognition to work.
Previously I tried haarcascades, however those were not as accurate and were very limited. Due to high performance needs, my Raspberyy Pi 3B+ was simply not enough. Thats when I settled for **server/client approach**. Rpi simply processed camera screen and sent it by **TCP** to the server, running the recognition model and responding with an array of the human rectangle coordinations. The reason I picked TCP rather than UDP was to have correctly ordered movement commands for mi rpi, although I am sure **this approach is not as efficient**.

## Result

**I successfully crafted two prototypes** of RpiTurret, I coded server and client sides communication and applied human recognition. The movement part did have some issues, however I blame it on little imperfections in the latest prototype.
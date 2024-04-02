# Notes

- Subset of a shuffled list

    ```ini
    # Set the color mode
    SetColorMode(
      # Normal distribute colors, because randomization is pretty
      NormalColorMode(
        # Arc around the center
        ArcColorMode(
          # Subset of provided colors, 10 colors, wrapping around
          getSubcolors(
            # Only use the first 4 colors
            subset(
              # Shuffle the array of colors
              shuffle(
                # Pick a color set
                choice([
                  ["#eaac43", "#ea4c65", "#1a2431","#57a37d","#cace9d","#527157"],
                  ["#ff0000","#ffa500","#ffff00","#008000","#0000ff","#4b0082","#ee82ee"],
                  ["#02d7f2","#f2e900","#007aff","#ff1111","#000000"],
                  ["#ffbe0b","#fb5607","#ff006e","#8338ec","#3a86ff"]
                ])
              ),
              0, 3
            ),
            10,
            true
          )
        ),
        mult(random(), "0.1"),
        mult(random(), "0.1")
      )
    )
    ```

- Moon

    ```ini
    # Set color mode
    SetColorMode(
      # Draw Polygons
      PolygonColorMode([
        # The dark side
        [
          NormalColorMode(
            ArcColorMode(
              getSubcolors(
                ["#ff0000","#ffa500","#ffff00","#008000","#0000ff","#4b0082","#ee82ee"],
                10,
                true
              ),
            ),
            mult(random(), "0.1"),
            mult(random(), "0.1")
          ),
          [['0.8181980515339464', '0.5'], ['0.8026243303837808', '0.6390576474687264'], ['0.757427631267958', '0.764503363531613'], ['0.6870321219998541', '0.8640576474687264'], ['0.5983286055009848', '0.9279754323328191'], ['0.5', '0.95'], ['0.3609423525312737', '0.9279754323328191'], ['0.23549663646838714', '0.8640576474687264'], ['0.13594235253127368', '0.764503363531613'], ['0.0720245676671809', '0.6390576474687264'], ['0.04999999999999999', '0.5'], ['0.0720245676671809', '0.3609423525312735'], ['0.13594235253127362', '0.23549663646838714'], ['0.23549663646838703', '0.13594235253127368'], ['0.3609423525312736', '0.0720245676671809'], ['0.49999999999999994', '0.04999999999999999'], ['0.5983286055009847', '0.07202456766718085'], ['0.687032121999854', '0.13594235253127357'], ['0.757427631267958', '0.23549663646838698'], ['0.8026243303837808', '0.36094235253127355']]
        ],
        # The main Circle
        [
          NormalColorMode(
            ArcColorMode(
              getSubcolors(
                ["#ffbe0b","#fb5607","#ff006e","#8338ec","#3a86ff"],
                10,
                true
              ),
            ),
            mult(random(), "0.1"),
            mult(random(), "0.1")
          ),
          [['0.95', '0.5'], ['0.9279754323328191', '0.6390576474687264'], ['0.8640576474687264', '0.764503363531613'], ['0.764503363531613', '0.8640576474687264'], ['0.6390576474687264', '0.9279754323328191'], ['0.5', '0.95'], ['0.3609423525312737', '0.9279754323328191'], ['0.23549663646838714', '0.8640576474687264'], ['0.13594235253127368', '0.764503363531613'], ['0.0720245676671809', '0.6390576474687264'], ['0.04999999999999999', '0.5'], ['0.0720245676671809', '0.3609423525312735'], ['0.13594235253127362', '0.23549663646838714'], ['0.23549663646838703', '0.13594235253127368'], ['0.3609423525312736', '0.0720245676671809'], ['0.49999999999999994', '0.04999999999999999'], ['0.6390576474687263', '0.07202456766718085'], ['0.7645033635316127', '0.13594235253127357'], ['0.8640576474687263', '0.23549663646838698'], ['0.9279754323328191', '0.36094235253127355']]
        ],
        # The background
        [
          "#000000",
          [[0,0],[1,0],[1,1],[0,1]]
        ]
      ])
    )
    ```
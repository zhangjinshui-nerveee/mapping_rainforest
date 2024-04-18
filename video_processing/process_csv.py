import pandas as pd

if __name__ == "__main__":
    video_file = "P0740368"
    df = pd.read_csv(f"{video_file}.csv", sep=' ', index_col=False)

    df.insert(loc=0, column='img_file', value=(df.index+1).astype(str))
    df['img_file'] = df['img_file'].apply(lambda x: 'Frame' + x.zfill(5) + '.jpg')

    print(df.head)

    df = df[['img_file', 'location_longitude', 'location_latitude', 'location_altitude_egm96amsl']]

    df.to_csv(f"{video_file}_modified.csv", index=False, sep='\t', header=False)


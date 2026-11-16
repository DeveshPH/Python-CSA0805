import csv, io, sqlite3, time, cProfile, pstats, statistics, random
try:
    import pandas as pd
except ImportError:
    pd = None

def loop_means(rows):
    acc = {}
    for station, day, value in rows:
        key=(station,day)
        total,count=acc.get(key,(0.0,0))
        acc[key]=(total+value,count+1)
    return {k:v[0]/v[1] for k,v in acc.items()}

def sql_means(rows):
    con=sqlite3.connect(":memory:")
    con.execute("CREATE TABLE r(station TEXT, day TEXT, pm REAL)")
    con.executemany("INSERT INTO r VALUES(?,?,?)", rows)
    result=dict(con.execute("SELECT station||'|'||day, AVG(pm) FROM r GROUP BY station,day"))
    con.close()
    return result

def pandas_means(rows):
    if pd is None: return None
    frame=pd.DataFrame(rows,columns=["station","day","pm"])
    return (frame.groupby(["station","day"])["pm"].mean()).to_dict()

def benchmark():
    random.seed(2)
    for stations in (1,12,120):
        rows=[]
        for s in range(stations):
            for day in range(365):
                for hour in range(24):
                    rows.append((f"S{s:03}",f"D{day:03}",random.uniform(0,200)))
        for name,fn in [("loop",loop_means),("sql",sql_means)] + ([("pandas",pandas_means)] if pd else []):
            start=time.perf_counter(); result=fn(rows); elapsed=time.perf_counter()-start
            print(stations,len(rows),name, f"{elapsed:.4f}s", len(result) if result is not None else "n/a")
        assert len(loop_means(rows)) == len(sql_means(rows))
    cProfile.run("loop_means(rows)", sort="cumtime")

if __name__ == "__main__":
    benchmark()

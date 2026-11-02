def usando_split(recebe:str):
    print(recebe.split())


def count_strip_split_join(recebe:str):
    print(' '.join(recebe))
    print(recebe.split())
    print(' '.join(recebe.split()))

if __name__ =="__main__":
	recebe="Nossa aula Manipulando String"
	usando_split(recebe)
	count_strip_split_join(recebe)

# -*- coding: utf-8 -*-

##################################
#  Automatic Book Classification #
##################################

import numpy as np


class Classifier:
    def __init__(self, _alpha, _beta):
        self.c_list = []  # category_list
        self.bk_list = []  # 도서명 자질 리스트
        self.k_list = []  # 키워드 자질 리스트
        self.bk_matrix = np.array([])  # 도서명 자질 빈도 matrix
        self.k_matrix = np.array([])  # 키워드 자질 빈도 matrix
        self.alpha = _alpha  # 도서명 자질 빈도 가중치
        self.beta = _beta  # 키워드 자질 빈도 가중치

    def learning(self, _books):
        # book = {Category, book_keyword[1, 2, 3], keyword[1, 2, 3}] // book 객체 스키마
        for book in _books:
            if book['category'] not in self.c_list:  # 카테고리 리스트 만들기 (비 중복)
                self.c_list.append(book['category'])
            for keyword in book['book_keywords']:  # 도서명 자질 리스트 만들기 (비 중복)
                if keyword not in self.bk_list:
                    self.bk_list.append(keyword)
            for keyword in book['keywords']:  # 키워드 자질 리스트 만들기(비 중복)
                if keyword not in self.k_list:
                    self.k_list.append(keyword)
        # 카테고리 수 X 도서명 자질 개수 shape의 이중리스트 생성, 0.0으로 초기화
        bk_doublelist = [[0.0] * len(self.bk_list) for _ in range(len(self.c_list))]
        # 카테고리 수 X 키워드 자질 개수 shape의 이중리스트 생성, 0.0으로 초기화
        k_doublelist = [[0.0] * len(self.k_list) for _ in range(len(self.c_list))]

        for book in _books:
            row_idx = self.c_list.index(book['category'])  # c_list에서 현재 책의 카테고리 인덱스를 구함 (이중리스트의 행 인덱스)

            for keyword in book['book_keywords']:  # 책의 도서명 자질을 모두 순회
                bk_column_idx = self.bk_list.index(keyword)  # bk_list에서 자질의 인덱스를 구함 (이중리스트의 열 인덱스)
                bk_doublelist[row_idx][bk_column_idx] += 1  # 셀의 값을 1 증가

            for keyword in book['keywords']:  # 책의 키워드 자질 3가지 모두 순회
                k_column_idx = self.k_list.index(keyword)  # k_list에서 자질의 인덱스를 구함 (이중리스트의 열 인덱스)
                k_doublelist[row_idx][k_column_idx] += 1  # 셀의 값을 1 증가

        bk_arr = np.array(bk_doublelist)  # 카테고리 X 도서명자질 이중리스트(2차원배열)를 행렬로 변환
        k_arr = np.array(k_doublelist)  # 카테고리 X 키워드자질 이중리스트(2차원배열)를 행렬로 변환

        # bk_arr(A1 x B1)의 각 행의 값을 전부 합한 행렬(B1 x 1)을 A1만큼 행 복제한 후 Transpose 해서 bk_arr 와 동일한 차원으로 만든다
        bk_sum_mat = np.array([np.sum(bk_arr, axis=1)] * bk_arr.shape[1]).T
        # k_arr(A2 x B2)의 각 행의 값을 전부 합한 행렬(B2 x 1)을 A2만큼 행 복제한 후 Transpose 해서 k_arr 와 동일한 차원으로 만든다
        k_sum_mat = np.array([np.sum(k_arr, axis=1)] * k_arr.shape[1]).T

        self.bk_matrix = bk_arr / bk_sum_mat  # 각 셀을 행의 총합으로 나눔, 즉 한 행에서의 빈도
        self.k_matrix = k_arr / k_sum_mat  # 각 셀을 행의 총합으로 나눔, 즉 한 행에서의 빈도

        return 0

    def exercise(self, bklist, klist):
        bk_vector = [0] * len(self.bk_list)
        k_vector = [0] * len(self.k_list)
        for book_keyword in bklist:
            if book_keyword in self.bk_list:
                bk_vector[self.bk_list.index(book_keyword)] += 1

        for keyword in klist:
            if keyword in self.k_list:
                k_vector[self.k_list.index(keyword)] += 1

        new_bkarr = np.array(bk_vector).T
        new_karr = np.array(k_vector).T

        bkresult = (self.alpha * (np.dot(self.bk_matrix,
                                         new_bkarr))).T  # bk_matrix(A1 X B1)와 new_bkarr(B1 X 1) 곱연산 후 alpha 가중치를 곱한 후 1 X A1로 Transpose
        kresult = (self.beta * (np.dot(self.k_matrix,
                                       new_karr))).T  # k_matrix(A2 X B2)와 new_karr(B2 X 1) 곱연산 후 beta 가중치를 곱한 후 1 X A2로 Transpose

        result = (bkresult + kresult).tolist()  # 두 결과를 합친 후 list로 변환
        return self.c_list[result.index(max(result))]  # 가장 큰 값의 index를 구함 c_list에 인덱스를 넣고 카테고리 추출


if __name__ == '__main__':  # 모듈 실행 테스트 코드

    books = [
        {"category": "컴퓨터", "book_keywords": ["키보드", "마우스", "모니터"], "keywords": ["프로그래밍", "주변기기", "하드웨어"]},
        {"category": "예술", "book_keywords": ["붓", "기법", "색"], "keywords": ["미술", "색채", "수채화"]},
        {"category": "예술", "book_keywords": ["붓", "색상", "그림체"], "keywords": ["그림", "물감", "유채화"]}
    ]

    new_bklist = ["키보드", "본체", "커피"]
    new_klist = ["가나", "책상", "유채화"]

    alpha = 0.5  # 도서명 자질 빈도 가중치 설정
    model = Classifier(alpha, 1 - alpha)  # 모델 객체 생성
    model.learning(books)  # 학습
    print model.exercise(new_bklist, new_klist)  # 모델에 의해 분류된 카테고리 명 출력

#include <vcl.h>
#include <iostream>
#include <list>
#include <algorithm>
#include <conio>
#include <queue>
#include <fstream>
#include <time.h>
using namespace std;
/**
*@file grafo.cpp
*Arquivo documentado
*/




/** @var typedef struct node *link
    *Estrutura node agora � chamada de link.
*/
/** @var typedef struct gnode *bins
    *Estrutura gnode agora � chamada de bins.
*/
/** @var typedef struct Glist *glist
    *Estrutura glist agora � chamada de Glist.
*/
/** @var typedef struct graph *Graph
    *Estrutura graph agora � chamada de Graph.
*/
/** @var typedef struct resp *Resp
    *Estrutura resp agora � chamada de Resp.
*/
/** @var typedef struct req *Req
    *Estrutura req agora � chamada de Req.
*/
/** @var typedef struct lreq *Lreq
    *Estrutura lreq agora � chamada de Lreq.
*/
/** @var typedef struct ordem *Ordem
    *Estrutura ordem agora � chamada de Ordem.
*/
/** @var typedef struct lord *Lord
    *Estrutura lord agora � chamada de Lord.
*/
/** @var typedef struct rf *Rf
    *Estrutura rf agora � chamada de Rf.
*/
/** @var typedef struct lrf *Lrf
    *Estrutura lrf agora � chamada de Lrf.
*/
/** @var int H
    *Variavel H global que representa o maior menor caminho de todas as requisi��es.
*/
/** @var int tamL
    *Variavel tamL que inicializada com o valor 0, e representa quantas requisi��es temos em uma instancia.
*/



typedef struct node *link;
typedef struct gnode *bins;
typedef struct Glist *glist;
typedef struct graph *Graph;
typedef struct resp *Resp;
typedef struct req *Req;
typedef struct lreq *Lreq;
typedef struct ordem *Ordem;
typedef struct lord *Lord;
typedef struct rf *Rf;
typedef struct lrf *Lrf;
Graph GRAPHinit(int V);
void GRAPHinsertArc(Graph G,int V,int **ad);
void desalocaMatriz(int ** r,int v);
int H=0,tamL=0,gu=INT_MAX;




/**
*Estrutura dos grafos
*/
struct gnode{
        /**
        *Grafo
        */
        Graph g;
        /**
        *Ponteiro para o proximo grafo*/
        bins next;
};


/**
*Estrutura da lista de grafos
*/
struct Glist{
        /**
        *Ponteiro que aponta para o inicio da lista de grafos.
        */
        bins ini;
        /**
        *Ponteiro que aponta para o fim da lista de grafos.
        */
        bins fim;

        int q;/**< Valor de numeros de grafos que foram criados.*/
};



/**
*Estrutura node
*/
struct node{
        int w; /**<Indice do n�.*/
        /**
        *Ponteiro para o proximo n�.
        */
        link next;
};


/**
*Estrutura de requisi�ao.
*/
struct ordem{
        int I;      /**<Indice do n� de origem da requisi��o.*/
        int O;       /**<Indice N� de destino da requisi��o*/
        int V;      /**<Tamanho do menor camiho encontrado na requisi��o*/
        int F;      /** <Fluxo maximo da requisicao */
        bool C;      /**<1 quando a requisi��o for atendida e 0 para quando nao for atendida*/
        /**
        *Ponteiro para a proxima requisi��o
        */
        Ordem prox;
        };

struct lord{
        /**
        *Ponteiro para o inicio das requisi��es
        */
        Ordem ini;
        };
/**
*Estrutura de grafo
*/
struct graph{
        int V;      /**<Numero de vertices do grafo.*/
        int A;      /**<Numero de arestas do grafo.*/
        int IG;     /**<Indice do grafo na lista de grafos.*/
        /**
        *Link de adjacentes do n�
        */
        link *adj;
};
/**
*Estrutura de resposta
*/
struct resp{
        int V;            /**<Tamanho do caminho encontrado.*/
        bool c;           /**<1 se o caminho foi encontrado e 0 se n�o foi.*/
        /**
        *Ponteiro para o caminho encontrado
        */
        link next;
};

/**
*Estrutura da lista de respostas
*/
struct req{
        int o; /**<N� de origem.*/
        int f; /**<N� de destino*/
        int ig;/**<Indice do grafo onde a requisi��o foi alocada */
        /**
        *Ponteiro para a estrutura contendo o caminho e o tamanho do caminho encontrado
        */
        Resp r;
        /**
        *Ponteiro para a proxima resposta.
        */
        Req prox;
};

struct lreq{
        int S;  /**<Somatorio dos caminhos encontrados.*/
        /**
        *Ponteiro paro o inicio da lista de respostas
        */
        Req ini;
        };
/**
*Estrutura de  respostas finais
*/
struct rf{
        int qg; /**<Quantidade de grafos utilizados.*/
        int sc; /**<Somatorios dos caminhos encontrados.*/
        float mc; /**<Tamanho medio dos caminhos.*/
        int tr;  /**<Numero total de requisi��es.*/
        /**
        *Ponteiro para a proxima resposta
        */
        Rf prox;
};


struct lrf{
        /**
        *Ponteiro para o Inicio da lista de respostas
        */
        Rf ini;
        int V; /**<Numero de vertices do grafo.*/
        int A; /**<Numero de arestas do grafo.*/
};


/*Fun��es para lista de resposta*/
/**
*Fun��o para criar uma lista vazia de Respostas de cada requisicao.
*@return de uma lista vazia
*/
Lreq criavazia(){
        Lreq l = new struct lreq;
        l->ini = NULL;
        l->S=0;
        return l;
}
/**
*@fn Lreq criareq(Lreq l, int i , int o , int id, Resp s,link z)
*Funcao para criar a resposta dos caminhos encotrandos
*@param l Lista de respostas
*@param i Inicio da requisicao
*@param o Destino da requisicao
*@param id Indice do grafo que a requisicao foi alocado
*@param s Lista com a resposta da requisicao
*@param z Lista com o caminho da requisicao
*@return Lista Lreq que aponta para o inicio das respostas
*/

Lreq criareq(Lreq l, int i , int o , int id, Resp s,link z){

        Req r = new struct req;
        r->o = i;
        r->f  = o;
        r->ig = id;
        r->r = s;
        r->r->next = z;
        r->prox = l->ini;
        l->ini = r;
        l->S=l->S+s->V;
                return l;

}

/**
*@fn Lrf cria()
*Funcao para inicializar a lista com as respostas finais
*@return lista de respostas finais vazia
*/


Lrf cria(){
        Lrf r = new struct lrf;
        r->ini = NULL;
        return r;
}


/**
*@fn int glist_vazia(glist l)
*Funcao para vereficar se a lista de grafos esta vazia
*@param l Lista de grafos
*@return 1 se estiver vazia e 0 se nao estiver
*/
int glist_vazia(glist l){
        if(l->ini == NULL ){
                if(l->fim == NULL)
                         return 1;
         }
        else
                return 0;}


/**
*@fn glist crialista()
*Funcao para criar uma lista de grafos
*@return 1 se estiver vazia e 0 se nao estiver
*/
glist crialista(){
        glist l = new struct Glist;
        l->ini =NULL;
        l-> fim =NULL;
        l->q=0;
        return l;
}


/**
*@fn link NEWnode( int w, link next)
*Funcao para criar um novo no
*@param w Indice do no a ser criado
*@param next Endereco do proximo no do grafo
*@return Endereco do novo no criado
*/
link NEWnode( int w, link next){
        link a= new struct node ;
        a->w=w;
        a->next=next;
        return a;
}


/**
*@fn NEWgnode(glist x,int v,int **adt)
*Funcao para criar um novo grafo
*@param x Lista para armazenar todos os grafos criados
*@param v Numero de vertices
*@param adt Matriz contendo os adjacentes
*@return Lista com os grafos incluindo o novo que foi criado
*/
glist NEWgnode(glist x,int v,int **adt){
        bins novo = new struct gnode;
        novo->next = NULL;
        novo->g = GRAPHinit(v);
        if(glist_vazia(x)){
                x->ini = novo;
                x->fim = novo;
                x->q++;
                novo->g->IG=x->q;
                GRAPHinsertArc(novo->g,v,adt);
                return x;
        }
        else
                x->fim->next = novo;
                x->fim = novo;
                x->q++;
                novo->g->IG=x->q;
                GRAPHinsertArc(novo->g,v,adt);
                return x;



}


/**
*@fn Graph GRAPHinit(int V)
*Funcao para iniciar um grafo
*@param V Numero de vertices
*@return Grafo inicializado
*/
Graph GRAPHinit(int V){
        Graph G = new struct graph;
        G->V=V;
        G->A=0;
        G->adj=new link[V];
        for (int v=0; v<V; ++v){
                G->adj[v]=NULL;
                }
        return G;
        }


/**
*@fn void GRAPHinsertArc(Graph G, int V,int **ad)
*Funcao para inserir os arcos no grafo
*@param G Grafo
*@param V Numero de vertices
*@param ad Matriz de ajacentes
*/
void GRAPHinsertArc(Graph G, int V,int **ad){
        int i,j;
        link aux;

/*inserindo os arcos no grafo*/
 for(i=0;i<V;i++){
 for(j=0;j<V;j++){
        if(ad[i][j]==1){
                if(G->adj[i]==NULL){
                        G->adj[i]=NEWnode(j+1 ,G->adj[i]);
                                G->A++;}
                else{
                for(aux=G->adj[i];aux!=NULL;aux=aux->next){
                if(aux->w != j+1){
                        G->adj[i]=NEWnode(j+1 ,G->adj[i]);
                        G->A++;
                        break;}
                }}

        }

   }
 }

        return;
}

/** @var typedef struct link2 Link2
    *Estrutura link2 agora � chamada de Link2.
*/
 typedef struct link2 Link2;

/**
*Estrutura usada na dijkstra
*/

struct link2
  {
    int dist;      /**<Valor da distancia do no atual para n� de inicio*/
    int visitado;  /**<Indicar se o n� foi visitado ou n�o*/
    int anterior;  /**<Indice do n� anterior*/
  };

/**
*@fn Resp dijkstra(int o, int f, Graph g)
*Funcao para achar o menor caminho
*@param o No de inicio
*@param f No de destino
*@param g Grafo
*@return Retorna uma lista resp com o caminho encontrado
*/

Resp dijkstra(int o, int f, Graph g)
  {
    Link2 *Q;
    int inf,menor, menor_id,tamQ;

    inf = g->V +1;
    Q = new Link2[g->V];
    tamQ = g->V;
    for (int i=0; i<g->V; i++)    /*colocando todos n�s como n�o visitado atualizando valores do n� anterios e da dist*/
      {
        if(i==o-1) Q[i].dist = 0;
        else Q[i].dist = inf;
        Q[i].visitado = 0;
        Q[i].anterior = -1;

      }
    menor_id = o;
    menor = 0;
    while((tamQ>0)&&(menor<inf))
      {
        for(link j = g->adj[menor_id-1]; j !=NULL; j = j->next)
          {
            if(!Q[j->w-1].visitado)
              {
                int dist_aux = Q[menor_id-1].dist + 1;
                if (dist_aux<Q[j->w-1].dist)
                  {
                    Q[j->w-1].dist = dist_aux;
                    Q[j->w-1].anterior = menor_id;
                  }
              }
          }
        Q[menor_id-1].visitado =1;
        if (menor_id == f) break;
        tamQ = tamQ-1;
        menor= g->V +1;
        if (tamQ >0)
          {
            for(int i = 0; i < g->V; i++)
              {
                if (!Q[i].visitado)
                  {
                    if (Q[i].dist < menor)
                      {
                        menor_id = i+1;
                        menor = Q[i].dist;
                      }
                  }
              }
          }
      }
      Resp r = new struct resp;
      if (Q[f-1].visitado)
        {
          r->V = Q[f-1].dist;
          r->c =1;
          r->next = NULL;

          int id = f;
          r->next = NEWnode(id,r->next);
          while(id !=o)
            {
              id = Q[id-1].anterior;
              r->next = NEWnode(id,r->next);
            }
        }
      else
        {
          r->V = g->V+1;
          r->c = 0;
          r->next = NULL;
        }

               delete []Q;
      return r;
    }
/**
*@fn exclui_aresta(Graph g , Resp r)
*Funcao para excluir aresta utilizada
*@param g Grafo no qual sera excluida a aresta
*@param r Arestas utilizadas
*/
void exclui_aresta(Graph g , Resp r){
        link i,j,k,t;
        int m;
        int ka;

        for(i=r->next, j= r->next->next; j!=NULL;i=j,j=j->next){
                m=i->w;

                for(k=g->adj[m-1]; k!=NULL; k=k->next){
                        t=k->next;
                        if(k->w== j->w || t->w == j->w){
                                if(g->adj[m-1]==k && k->w==j->w){

                                link aux = k;
                                g->adj[m-1]=k->next;
                                delete aux;}
                                else if(t->w == j->w && t->next!=NULL){
                                        link aux = t;
                                        k->next=t->next;
                                        delete aux;
                                }
                                else if(t->w == j->w && t->next==NULL ){
                                        link aux = t;
                                        k->next=NULL;
                                        delete aux;

                                }
                                break;
                                }
                }
        }

}
/**
*@fn requisicoes(int V,int **r,int **ad)
*Funcao que calculo o caminho minimo das requisicoes e cria lista de requisicoes
*@param V Numero de vertices
*@param r Matriz contendo as requisi�oes
*@param ad Matriz de adjacentes
*@return Lista de requisicoes
*/

Lord requisicoes(int V,int **r,int **ad){
glist O;
O=crialista();
O=NEWgnode(O,V,ad);
link q;
int i,j;
Lord Vord = new struct lord;
Vord->ini=NULL;
Ordem l;
int **or=new int*[V];
for(i=0;i<V;i++){
        or[i] = new int[V];
        }

int **rq=new int*[V];
for(i=0;i<V;i++){
        rq[i] = new int[V];
        }
for(i=0;i<V;i++){
   for(j=0;j<V;j++){
        rq[i][j]=r[i][j];
           }
}


for(i=0;i<V;i++){
   for(j=0;j<V;j++){
        if(r[i][j]!=0){
        or[i][j]=1;}
        else
                or[i][j]=0;
   }
}
/*criando a lista de requisi��es*/
for(i=0;i<V;i++){
        for(j=0;j<V;j++){
                while(or[i][j]!=0){/*achando um caminho para apenas uma requisi��o para da par de origem e destino*/
                Resp ord = new struct resp;
                ord = NULL;
                ord=dijkstra(i+1,j+1,O->ini->g);
                if(ord->c==1){
                        or[i][j]--;
                        while(rq[i][j]!=0){/*criando a lista de requisi��es com todas as requisi��es de cada par de origem e destino*/
                                Ordem OR= new struct ordem;
                                OR->I=i+1;
                                OR->O=j+1;
                                OR->V=ord->V;
                                OR->C=1;
                                OR->F=0;
                                OR->prox=Vord->ini;
                                Vord->ini = OR;
                                rq[i][j]--;
                                tamL++;
                                }
                        }
                }

        }
}
 desalocaMatriz(or,V);
 desalocaMatriz(rq,V);

return Vord;
}

/**
*@fn desalocalink(link a)
*Funcao para desalocar lista de inteiros(link).
*@param a Lista que vai desalocada.
*/

void desalocalink(link a){
link aux = a;
link del;
while(aux != NULL ){
        del = aux;
        aux = aux->next;
        delete del ;
}
delete aux;
}

/**
*@fn desalocaGrafo(Graph g, int v)
*Funcao para desalocar grafo .
*@param g Grafo a ser desalocado.
*@param v Numero de vertices.
*/

desalocaGrafo(Graph g, int v){

link aux;
int i ;
for (i=0;i<v;i++){
        desalocalink(g->adj[i]);

}
delete []g->adj;

delete g;
}

/**
*@fn desalocaglist(glist B)
*Funcao para desalocar lista de grafo .
*@param B lista de grafo a ser desalocado.
*/

desalocaglist(glist B){
bins aux,del;
aux = B->ini;

while(aux != NULL ){
        del = aux;
        aux = aux->next;
        desalocaGrafo(del->g,del->g->V);
}
delete aux;
delete B->ini;
delete B->fim;
delete B;
}


/**
*@fn desalocaLord(Lord l)
*Funcao para desalocar lista de requisicao .
*@param l lista de requisicao a ser desalocada.
*/
void desalocaLord(Lord l){
Ordem aux=l->ini;
Ordem del;
while(aux != NULL ){
        del = aux;
        aux = aux->prox;
        delete del ;
}

delete l;

}
/**
*@fn desalocaResp(Resp r)
*Funcao para desalocar a requisicao .
*@param r Requisicao a ser desalocada.
*/
void desalocaResp(Resp r){

desalocalink(r->next);

delete r;
}


/**
*@fn desalocaLreq(Lreq l)
*Funcao para desalocar a lista de respostas .
*@param l Lista de respostas a ser desalocada.
*/
void desalocaLreq(Lreq l){
Req aux=l->ini;
Req del;

for(Req i=l->ini;i!=NULL;i=i->prox){
desalocaResp(i->r);
}
while(aux != NULL ){
        del = aux;
        aux = aux->prox;
        delete del ;

}
delete l;

}

/**
*@fn desalocaLrf(Lrf l)
*Funcao para desalocar a lista de respostas final .
*@param l Lista de respostas final a ser desalocada.
*/
void desalocaLrf(Lrf l){
Rf aux=l->ini;
Rf del;
/*while(aux != NULL ){
        del = aux;
        if(aux->prox!=NULL){
        aux = aux->prox;}
        delete del ;

}*/
delete aux;
delete l;
}

/**
*@fn Lord randomiza (Lord l)
*Funcao para que randomiza a lista de requisicao.
*@param l Lista de requisicao a ser randomizada.
*@return Retorna a lista de requisicao randomizada
*/
Lord randomiza (Lord l){
int * rd = new int[tamL];
int i,x,aux;

for(i=0;i<tamL;i++){
        rd[i] = i+1; /* inicializa o vetor com as posic�es da lista*/
}
for(i=0;i<tamL ;i++){
        x = (rand()%(tamL-1)); //gera numero aleatorio de 1 ate tamL
        aux = rd[i];
        rd[i]= rd[x];
        rd[x] = aux;
}

Lord Vord = new struct lord;
Vord->ini=NULL;
Ordem j; int cnt;
int AR=0;
for(i=0;i<tamL;i++){
        x= rd[i]; /*vai inserir a posi��o X da lista na nova lista*/

        for(j=l->ini,cnt=1;j!=NULL;j=j->prox,cnt++) {
                if(cnt == x){     /*percorre a lista ate a posi��o desejada*/
                        Ordem OR= new struct ordem;  /* vai copiar as informa�oes para um novo struct Ordem*/
                        OR->I=j->I;
                        OR->O=j->O;
                        OR->V=j->V;
                        OR->C=1;
                        OR->prox=Vord->ini;
                        Vord->ini = OR;
                        break;
                }
        }
}

desalocaLord(l); /*desaloca a lista q estava sequencial*/
delete []rd;
return Vord;   /*retorna a nova lista randomizada*/

}


/**
*@fn Lord ordena(Lord l)
*Funcao para que ordenada a lista de requisicao.
*@param l Lista de requisicao a ser ordenada.
*@return Retorna a lista de requisicao ordenada.
*/
Lord ordena(Lord l){
int r,t,y,f;
Ordem k,i;
for(i=l->ini;i!=NULL;i=i->prox){
        for(Ordem j= i->prox;j!=NULL;j=j->prox){

                if(i->V < j->V){/*conferindo se o tamanho do caminho minimo da requisi�o � menor que o da proxima requisi��o na lista de requisi��es*/

                        r=i->I;
                        t=i->O;
                        y=i->V;
                        f=i->F;
                        i->I=j->I;
                        i->O=j->O;
                        i->V=j->V;
                        i->F=j->F;
                        j->I = r;
                        j->O = t;
                        j->V = y;
                        j->F=f;
                        }
                }

}
H=l->ini->V;


return l;
}
/**
*@fn Lord fmax(Lord l,int **ad,int V)
*Funcao para encontrar o fluxo maximo de cada requisicao.
*@param l Lista de requisicao.
*@param ad matriz de adjacentes.
*@param V numero de vertices.
*@return Retorna a lista de requisicoe.
*/

Lord fmax(Lord l,int **ad,int V){
Graph G;
Ordem a,aux;
int f=0,w=1,I,O,h;
h=0;
Resp road;
G=GRAPHinit(V);
GRAPHinsertArc(G,V,ad);
for(a=l->ini;a!=NULL;a=a->prox){
        if(h < a->V){
                h=a->V;}

        if(a->F==0){
                while(w==1){
                        I=a->I;
                        O=a->O;
                        road=dijkstra(I,O,G);
                        if(road->c==1){
                                exclui_aresta(G,road);
                                f++;
                                desalocaResp(road);
                        }
                        else{
                                desalocaResp(road);
                                w=0;
                            }
                }
                //cout<<"\nF:"<<f;
                for(aux=a;aux!=NULL;aux=aux->prox){
                        if(aux->I==I&&aux->O==O){
                                aux->F=f;
                }
          else{
                break;
          }

        }
        if(G!=NULL){
                desalocaGrafo(G,G->V);
        }
        if(w==0){
                G=GRAPHinit(V);
                GRAPHinsertArc(G,V,ad);
        }
        f=0;
        w=1;

        }

}
cout<<"\nAcabei fluxo.";
H=h;
return l;
}

/**
*@fn Lord ordenaF(Lord l)
*Funcao para ordenar a lista de requisicao de acordo com o fluxo.
*@param l Lista de requisicao.
*@return Retorna a lista de requisicoe.
*/

Lord ordenaF(Lord l){
int r,t,y,f,h;

Ordem k,i;
for(i=l->ini;i!=NULL;i=i->prox){
        for(Ordem j= i->prox;j!=NULL;j=j->prox){
                if(i->F < j->F){
                        r = i->I;
                        t = i->O;
                        y = i->V;
                        f = i->F;
                        i->I = j->I;
                        i->O = j->O;
                        i->V = j->V;
                        i->F = j->F;
                        j->I = r;
                        j->O = t;
                        j->V = y;
                        j->F = f;

                }
                else if(i->F==j->F && i->V<j->V){/*conferindo se o tamanho do caminho minimo da requisi�o � menor que o da proxima requisi��o na lista de requisi��es*/

                        r = i->I;
                        t = i->O;
                        y = i->V;
                        f = i->F;
                        i->I = j->I;
                        i->O = j->O;
                        i->V = j->V;
                        i->F = j->F;
                        j->I = r;
                        j->O = t;
                        j->V = y;
                        j->F = f;
                        }
                }

}


return l;
}
/**
*@fn desalocaMatriz(int ** r,int v)
*Funcao para que desaloca uma lista de inteiros.
*@param r Matriz a ser desalocada.
*@param v Dimensao da matriz.
*/

void desalocaMatriz(int ** r,int v){
int i;

for(i=0;i<v;i++){
        delete r[i];

}
delete []r;
}


/**
*@fn imprime_link(link a)
*Funcao para imprimir lista de inteiros(link).
*@param a Lista de Inteiros.
*/
void imprime_link(link a){
 link aux;
 cout << "\n Caminho : ";
 for(aux =a ;aux!=NULL; aux = aux->next)
        cout << " " << aux->w   ;
}

/**
*@fn imprime_resp (Resp r)
*Funcao para imprimir resposta.
*@param r Respostas.
*/
void imprime_resp (Resp r){
cout << "\nTamanho do caminho : "<< r->V ;
imprime_link(r->next);
}

/**
*@fn imprime_req (Lreq l)
*Funcao para imprimir lista de resposta.
*@param l Lista de respostas.
*/
void imprime_req(Lreq l){
int soma=0;
Req aux;
cout << "\n\n Lista de Resposta\n" ;
for(aux=l->ini;aux!=NULL;aux = aux->prox){
cout<< "\n\n";
cout << "\n Origem: "<< aux->o;
cout << "\n Destino: "<< aux->f;
cout <<"\n Indice grafo: "<< aux->ig;
soma=aux->r->V+soma;
imprime_resp(aux->r);
}
cout<<"\n\n\nSomatorio:"<<soma;
cout<<"\nTamanho:"<<tamL;
cout<<"\nH:"<<H;
}



/**
*@fn kapov(Lord k,glist A,int v,int **ad,Lreq rr)
*Funcao que executa o metodo desenvolvido por Kapov.
*@param k Lista de requisicao ordenada.
*@param A Lista de grafos.
*@param v Numero de vertices.
*@param ad Matriz de adjacencia.
*@param rr Lista de respostas.
*@return Lista de resposta
*/
Lreq kapov(Lord k,glist A,int v,int **ad,Lreq rr){
bins aux;
int i,j;
link te;
Ordem l;
int soma=0;
Resp road;
for(l=k->ini;l!=NULL;l=l->prox){
        i=l->I;
        j=l->O;
        road = NULL;
        aux=A->ini;
        link z;
        while(l->C){
                road=dijkstra(i,j,aux->g);
                if(road->V <= H){           /*caso tenha caminho e seja menor que o H*/
                        exclui_aresta(aux->g, road);
                        l->C=0;
                        z= road->next;
                        rr = criareq(rr,l->I,l->O,aux->g->IG,road,z); /* */
                        }
                /*percorrendo a lista de grafos*/
                else if(road->V > H && aux->next!=NULL){          /*caso o caminha achado seja maior que H e tenha um proximo grafo*/
                        aux=aux->next;
                        desalocaResp(road);
                        }
                /*cria��o de novos grafos*/
                else if(road->V > H && aux->next==NULL){   /*caso o caminho achado seja maior que H e nao tenha um proximo grafo*/
                        if(A->q==gu-1){
                                desalocaResp(road);
                                desalocaglist(A);
                                desalocaLreq(rr);
                                return NULL;
                                }
                        else{
                                desalocaResp(road);
                                A=NEWgnode(A,v,ad);
                                aux=A->fim;
                                }
                        }

                }
}
if(A->q<gu){
gu = A->q;
}


return rr;
}





/**
*@fn gulosa(Lord k,glist A,int v,int **ad,Lreq rr)
*Funcao que executa o metodo guloso.
*@param k Lista de requisicao ordenada.
*@param A Lista de grafos.
*@param v Numero de vertices.
*@param ad Matriz de adjacencia.
*@param rr Lista de respostas.
*@return Lista de resposta
*/
Lreq gulosa(Lord k,glist C,int V,int **ad,Lreq rr){
bins aux;
int i,j;
Ordem l;
int soma=0;
Resp road;
for(l=k->ini;l!=NULL;l=l->prox){
        i=l->I;
        j=l->O;
        aux=C->ini;
        link z;
        while(l->C){
                road=dijkstra(i,j,aux->g);
                if(road->c==1){
                        exclui_aresta(aux->g, road);
                        l->C=0;

                        z= road->next;
                        rr = criareq(rr,l->I,l->O,aux->g->IG,road,z);
                        }
                else if(road->c==0 && aux->next!=NULL){
                        aux=aux->next;
                        }
                else if(road->c==0 && aux->next == NULL){
                        C=NEWgnode(C,V,ad);
                        aux=C->fim;
                        }
                }
}


return rr;
}


/**
*@fn Lkapov(Lord Lordena, int v, int **ad, int **r)
*Funcao que cria a lista de resposta final.
*@param Lordena Lista de requisicao ordenada.
*@param v Numero de vertices.
*@param ad Matriz de adjacencia.
*@param r Matriz de requisicao.
*@return Lista final de resposta
*/
Lrf Lkapov(Lord Lordena, int v, int **ad, int **r){
Lrf fr;
float tempo=0;
glist B;
Lreq lr;
time_t  t_ini, t_fim;
int GU=INT_MAX;
fr=cria();
Rf R= new struct rf;
t_ini= time(NULL);

while(tempo<300){
        B=crialista();
        B=NEWgnode(B,v,ad);

        lr=criavazia();

        lr = kapov(Lordena, B,v,ad,lr);

        if(lr==NULL){

                Lordena = randomiza(Lordena);
                //Lordena = ordena(Lordena);
                Lordena = ordenaF(Lordena);
        }
        else{
                if(B->q<GU){
                        R->qg=B->q;
                        R->sc=lr->S;
                        R->mc= (float)R->sc/(float)tamL;
                        R->tr=tamL;
                        R->prox=fr->ini;
                        fr->ini=R;
                        R->prox=NULL;
                        fr->V=v;
                        fr->A=B->ini->g->A;
                        }
                Lordena = randomiza(Lordena);
                Lordena = ordena(Lordena);
                //Lordena = ordenaF(Lordena);

                desalocaglist(B);
                desalocaLreq(lr);
        }
        t_fim= time(NULL);
        tempo=difftime(t_fim,t_ini);
}
cout<<"\nTempo:"<<tempo;


desalocaLord (Lordena);
return fr;
}

/**
*@fn Lgulosa(Lord Lordena, int v, int **ad, int **r)
*Funcao que cria a lista de resposta final.
*@param Lordena Lista de requisicao ordenada.
*@param v Numero de vertices.
*@param ad Matriz de adjacencia.
*@param r Matriz de requisicao.
*@return Lista final de resposta
*/
Lrf Lgulosa(Lord Lordena, int v, int **ad){
Lrf fr;
float tempo;
glist B;
Lreq lr;
time_t  t_ini, t_fim;

fr=cria();

t_ini= time(NULL);

while(tempo<300){
        B=crialista();
        B=NEWgnode(B,v,ad);

        lr=criavazia();
        lr = gulosa(Lordena, B,v,ad,lr);
        Rf R= new struct rf;

        R->qg=B->q;
        R->sc=lr->S;
        R->mc= (float)R->sc/(float)tamL;
        R->tr=tamL;
        R->prox=fr->ini;
        fr->ini=R;
        fr->V=v;

        Lordena = randomiza(Lordena);
        Lordena = ordena(Lordena);

        desalocaglist(B);
        desalocaLreq(lr);
        t_fim= time(NULL);
        tempo=difftime(t_fim,t_ini);
        cout<<"\nTempo:"<<tempo;
}

desalocaLord (Lordena);
return fr;
}

/**
*@fn criatxtK(Lrf R)
*Funcao que cria arquivo .txt com as respostas.
*@param R Lista de resposta final.

*/
void criatxtK(Lrf R){

int k,q,w,i;
float e;

Rf a= R->ini;
std::ofstream file1 ("C:\\Users\\Artur Alvarenga\\Documents\\GitHub\\RACO\\Resultados\\dadosgiul.txt");
file1<<"\nNumero de vertices:"<<R->V;
file1<<"\nNumero de arestas:"<<R->A;
file1<<"\n\n";
file1<<"\nNumero de grafos:"<<a->qg;
file1<<"\nSomatorio dos caminhos:"<<a->sc;
file1<<"\nMedia dos caminhos:"<<a->mc;
file1<<"\nTotal de requisi��es:"<<a->tr;
file1<<"\n\n";


file1.close();
}


/**
*@fn criatxtG(Lrf R)
*Funcao que cria arquivo .txt com as respostas.
*@param R Lista de resposta final.

*/
void criatxtG(Lrf R){
int k,q,w,i;
float e;
for(Rf a=R->ini;a!=NULL;a=a->prox){
        for(Rf b=a->prox;b!=NULL;b=b->prox){
                if(a->qg > b->qg){
                k=b->qg;
                q=b->sc;
                e=b->mc;
                w=b->tr;
                b->qg=a->qg;
                b->sc=a->sc;
                b->mc=a->mc;
                b->tr=a->tr;
                a->qg=k;
                a->sc=q;
                a->mc=e;
                a->tr=w;
                }
                }

}
Rf a= R->ini;
std::ofstream file1 ("dadosGbrasil.txt");
        file1<<"\nNumero de vertices:"<<R->V;
        file1<<"\n\n";
        for(i=0;i<10;i++){
        file1<<"\nNumero de grafos:"<<a->qg;
        file1<<"\nSomatorio dos caminhos:"<<a->sc;
        file1<<"\nMedia dos caminhos:"<<a->mc;
        file1<<"\nTotal de requisi��es:"<<a->tr;
        file1<<"\n\n";
        a=a->prox;
        if(a==NULL){
                break;
                }

}

file1.close();
}





/**Main*/
int main(){
int v,y,i,j,k,q,w;
float e;
link te;
srand(NULL);




/*leitura do arquivo com o numero de nos*/
std::ifstream file ("C:\\Users\\Artur Alvarenga\\Documents\\GitHub\\RACO\\Inst�ncias\\giul.txt");

if(!file){
        printf("\n Erro de leitura.");
        return 0;}
file>>v;

int **ad= new int*[v];
 for(i=0;i<v;i++){
        ad[i] = new int[v];
}


int **r =new int*[v];
for(i=0;i<v;i++){
        r[i] = new int[v];
        }

for(i=0;i<v;i++){
   for(j=0;j<v;j++){
        file>>ad[i][j];
   }

}

for(i=0;i<v;i++){
   for(j=0;j<v;j++){
        file>>r[i][j];
   }
}


file.close();


srand(time(0));

Lord Lordena= requisicoes(v,r,ad);
Ordem l;
Lordena = fmax(Lordena,ad,v);
Lordena = randomiza(Lordena);
//Lordena = ordena(Lordena);
Lordena = ordenaF(Lordena);

Lrf L;

L=Lkapov(Lordena,v,ad,r);
criatxtK(L);
//L=Lgulosa(Lordena,v,ad);
//criatxtG(L);





desalocaLrf(L);
desalocaMatriz(r,v);
desalocaMatriz(ad,v);
cout<<"\nAcabei";
getch();

        return 0;
}


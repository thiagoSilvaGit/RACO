#include <vcl.h>
#include <iostream>
#include <list>
#include <algorithm>
#include <conio>
#include <queue>
#include <fstream>
using namespace std;


typedef struct queue *QUEUE;
typedef struct node *link;
typedef struct gnode *bins;
typedef struct Glist *glist;
typedef struct graph *Graph;
typedef struct resp *Resp;
typedef struct req *Req;
typedef struct lreq *Lreq;
typedef struct ordem *Ordem;
typedef struct lord *Lord;
Graph GRAPHinit(int V);
void GRAPHinsertArc(Graph G,int V,int **ad);
void desalocaMatriz(int ** r,int v);
int H,tamL=0;


/*estruturas*/

/*struct dos grafos*/
struct gnode{
        Graph g;       /*Estruras de grafos contendo um grafo e o prximo*/
        bins next;
};


/*strut da lista de grafos*/
struct Glist{
        bins ini;  /*Grafo de inicio da lista*/
        bins fim;  /*Grafo de fim da lista*/
        int q;     /*Quantidade de grafos na lista*/
};



/*struct do nó*/
struct node{
        int w;          /*Indice do nó*/
        link next;      /*link para o proximo nó*/
};


/*struct de requisiçao*/
struct ordem{
        int I;       /*Nó de inicio da requisição*/
        int O;       /*Nó de destino da requisição*/
        int V;       /*Tamanho da requisição*/
        bool C;      /*0 quando a requisição for atendida e 1 para quando nao for atendida*/
        Ordem prox;  /**/
        };

struct lord{
        Ordem ini; /**/
        };
/*struct de grafo*/
struct graph{
        int V;      /*numero de vertices do grafo*/
        int A;      /*numero de arestas do grafo*/
        int IG;     /*indice do grafo*/
        link *adj;  /*lista de adjacentes do grafo*/
};
/*struct de resposta*/
struct resp{
        int V;            /*tamanho do caminho encontrado*/
        bool c;           /*Se o caminho foi encontrado ou nao*/
        link next;        /*Lista com os nós do caminho encontrado*/
};

/*lista de resposta*/
struct req{
        int o;
        int f;
        int ig;
        Resp r;
        Req prox;
};

struct lreq{
        Req ini;
        };

/*Funções para lista de resposta*/

Lreq criavazia(){
        Lreq l = new struct lreq;
        l->ini = NULL;
        return l;
}

Lreq criareq(Lreq l, int i , int o , int id, Resp s,link z){

        Req r = new struct req;
        r->o = i;
        r->f  = o;
        r->ig = id;
        r->r = s;
        r->r->next = z;
        r->prox = l->ini;
        l->ini = r;
                return l;

}




/*funções para lista*/

/*função para verificar se a lista está vazia*/
int glist_vazia(glist l){
        if(l->ini == NULL ){
                if(l->fim == NULL)
                         return 1;
         }
        else
                return 0;}


/*função para criar lista*/
glist crialista(){
        glist l = new struct Glist;
        l->ini =NULL;
        l-> fim =NULL;
        l->q=0;
        return l;
}


/*função para criar um novo nó*/
static link NEWnode( int w, link next){
        link a= new struct node ;
        a->w=w;
        a->next=next;
        return a;
}


/*funçao de criar um novo grafo*/
static glist NEWgnode(glist x,int v,int **adt){
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


/*iniciar um grafo*/
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


/*Função para inserir os arcos*/
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


 typedef struct link2 Link2;

struct link2
  {
    int dist;      /*valor da distancia do no atual para nó de inicio*/
    int visitado;  /*indicar se o nó foi visitado ou não*/
    int anterior;  /*indice do nó anterior*/
  };

Resp dijkstra(int o, int f, Graph g)
  {
    Link2 *Q;
    int inf,menor, menor_id,tamQ;

    inf = g->V +1;
    Q = new Link2[g->V];
    tamQ = g->V;
    for (int i=0; i<g->V; i++)    /*colocando todos nós como não visitado atualizando valores do nó anterios e da dist*/
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
      return r;
    }



/*funçao para excluir o caminho utilizado*/
void exclui_aresta(Graph g , Resp r){
cout<<"\n exclui aresta";
        link i,j,k;
        int m;
        for(i=r->next, j= r->next->next; j!=NULL;i=j,j=j->next){
                m=i->w;
                for(k=g->adj[m-1]; k!=NULL; k=k->next){
                        if(k->w== j->w){
                                link aux = k;
                                g->adj[m-1]= k ->next;
                                free (aux);
                                break;
                                }
                }
        }

}
/*criando estrutura de requisiçoes*/

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
/*criando a lista de requisições*/
for(i=0;i<V;i++){
        for(j=0;j<V;j++){
                while(or[i][j]!=0){/*achando um caminho para apenas uma requisição para da par de origem e destino*/
                Resp ord = new struct resp;
                ord = NULL;
                ord=dijkstra(i+1,j+1,O->ini->g);
                if(ord->c==1){
                        or[i][j]--;
                        while(rq[i][j]!=0){/*criando a lista de requisições com todas as requisições de cada par de origem e destino*/
                                Ordem OR= new struct ordem;
                                OR->I=i+1;
                                OR->O=j+1;
                                OR->V=ord->V;
                                OR->C=1;
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

/*desaloca link*/
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

/*Desalocar grafo*/

desalocaGrafo(Graph g, int v){

link aux;
int i ;
for (i=0;i<v;i++){
        desalocalink(g->adj[i]);

}
delete g->adj;

delete g;

}

/*Desalocar lista de grafo*/

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


/* Desalocar a Lord*/
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

/*Randomizar a lista de requisiçoes*/
Lord randomiza (Lord l){
int * rd = new int[tamL];
int i,x,aux;
cout<<"\nVetor sem ordenar\n\n";
for(i=0;i<tamL;i++){
        rd[i] = i+1; /* inicializa o vetor com as posicões da lista*/
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
for(i=0;i<tamL;i++){
        x= rd[i]; /*vai inserir a posição X da lista na nova lista*/

        for(j=l->ini,cnt=1;j!=NULL;j=j->prox,cnt++) {
                if(cnt == x){     /*percorre a lista ate a posição desejada*/
                        Ordem OR= new struct ordem;  /* vai copiar as informaçoes para um novo struct Ordem*/
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


/*Ordenando a lista de requisiçoes*/
Lord ordena(Lord l){
int r,t,y;
Ordem k,i;
for(i=l->ini;i!=NULL;i=i->prox){
        for(Ordem j= i->prox;j!=NULL;j=j->prox){

                if(i->V < j->V){/*conferindo se o tamanho do caminho minimo da requisiço é menor que o da proxima requisição na lista de requisições*/

                        r=i->I;
                        t=i->O;
                        y=i->V;
                        i->I=j->I;
                        i->O=j->O;
                        i->V=j->V;
                        j->I = r;
                        j->O = t;
                        j->V = y;
                        }
                }

}
H=l->ini->V;
cout<<"\nH: "<<H;

return l;
}

/*desaloca matriz*/

void desalocaMatriz(int ** r,int v){
int i;

for(i=0;i<v;i++){
        delete r[i];

}
delete []r;
}



void imprime_link(link a){
 link aux;
 cout << "\n Caminho : ";
 for(aux =a ;aux!=NULL; aux = aux->next)
        cout << " " << aux->w   ;
}

void imprime_resp (Resp r){
cout << "\nTamanho do caminho : "<< r->V ;
imprime_link(r->next);
}


void imprime_req(Lreq l){

Req aux;
cout << "\n\n Lista de Resposta\n" ;
for(aux=l->ini;aux!=NULL;aux = aux->prox){
cout<< "\n\n";
cout << "\n Origem: "<< aux->o;
cout << "\n Destino: "<< aux->f;
cout <<"\n Indice grafo: "<< aux->ig;
 imprime_resp(aux->r);


}

}



/*metodo kapov*/
Lreq kapov(Lord k,glist A,int v,int **ad,Lreq rr){
bins aux;
int i,j;
link te;
Ordem l;
int soma=0;
for(l=k->ini;l!=NULL;l=l->prox){
        i=l->I;
        j=l->O;
        Resp road = new struct resp;
        road = NULL;
        aux=A->ini;
        link z;
        while(l->C){
                road=dijkstra(i,j,aux->g);
                /*cout<<"\n tem caminho de " <<l->I <<" para "<<l->O <<": "<<road->c;
                for(te=road->next;te!=NULL;te=te->next){
                cout<<"\nC:"<<te->w;}
                cout<<"\nTamanho: "<<road->V;*/
                if(road->c==1 && road->V <= H){           /*caso tenha caminho e seja menor que o H*/
                        exclui_aresta(aux->g, road);
                        l->C=0;
                        soma=soma+road->V;
                        /*cout<<"\nIG:"<<aux->g->IG;*/
                        z= road->next;
                        rr = criareq(rr,l->I,l->O,aux->g->IG,road,z); /* */
                        }
                /*percorrendo a lista de grafos*/
                else if(road->V > H && aux->next!=NULL){          /*caso o caminha achado seja maior que H e tenha um proximo grafo*/
                        /*cout<<"\nENTREI E FUI PARA O PROXIMO GRAFO";
                        cout<<"\nIndice do grafo que nao tem caminho:"<<aux->g->IG;*/
                        aux=aux->next;
                        }
                /*criação de novos grafos*/
                else if(road->V > H && aux->next==NULL){   /*caso o caminho achado seja maior que H e nao tenha um proximo grafo*/
                        A=NEWgnode(A,v,ad);
                        /*GRAPHinsertArc(A->ini->g,v);*/
                        aux=A->fim;
                        }

                cout<<"\nG:"<<A->q;
                }
}

cout<<"\nSomatorio:"<<soma;
cout<<"\nTamanho:"<<tamL;
cout<<"\n H:"<<H;

return rr;
}






Lreq gulosa(Lord k,glist C,int V,int **ad,Lreq rr){
bins aux;
int i,j;
link te;
Ordem l;
int soma=0;

for(l=k->ini;l!=NULL;l=l->prox){
        i=l->I;
        j=l->O;
        Resp road = new struct resp;
        road = NULL;
        aux=C->ini;
        link z;
        while(l->C){
                road=dijkstra(i,j,aux->g);
                /*printf("\n tem caminho de %d para %d: %d",l->I,l->O, road->c);*/
                /*for(te=road->next;te!=NULL;te=te->next){
                printf("\nC:%d",te->w);}*/
                cout<<"\nTamanho: "<<road->V;
                if(road->c==1){
                        exclui_aresta(aux->g, road);
                        l->C=0;
                        soma=soma+road->V;
                        z= road->next;
                        rr = criareq(rr,l->I,l->O,aux->g->IG,road,z);
                        }
                else if(road->c==0 && aux->next!=NULL){
                        aux=aux->next;
                        }
                else if(road->c==0 && aux->next == NULL){
                        C=NEWgnode(C,V,ad);
                        /*GRAPHinsertArc(C->ini->g,V);*/
                        aux=C->fim;
                        }
                printf("\nG:%d",C->q);
                }
}
cout<<"\nSomatorio:"<<soma;
cout<<"\nTamanho:"<<tamL;
cout<<"\n H:"<<H;

}



int main(){
glist B;
int v,y,i,j;
link te;
Lreq lr;

/*leitura do arquivo com o numero de nos*/
std::ifstream file ("nsf3.txt");

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


B=crialista();
B=NEWgnode(B,v,ad);

Lord Lordena= requisicoes(v,r,ad);
Ordem l,k;
Lordena = randomiza(Lordena);
Lordena = ordena(Lordena);

/*mostrando a lista de requisiçoes ordenada*/
for(k=Lordena->ini; k!=NULL; k=k->prox){
        cout << "\n\n\nOrigem: "<< k->I;
        cout << "\nDestino: " << k->O;
        cout << "\nTamanho: " << k->V;
        }

lr = kapov(Lordena, B,v,ad,lr);
/*lr = gulosa(Lordena,B,v,lr);*/

imprime_req(lr);






desalocaglist(B);
desalocaLord (Lordena);
desalocaMatriz(r,v);
desalocaMatriz(ad,v);
getch();

        return 0;
}

